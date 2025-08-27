from typing import Any, Dict, List, Optional, Type, TypeVar, Union
from datetime import datetime
import json
import sqlite3
from pathlib import Path
import threading
import queue
import logging
from contextlib import contextmanager

T = TypeVar('T')

class DatabaseError(Exception):
    """Base exception for database operations."""
    pass

class ConnectionError(DatabaseError):
    """Exception for connection-related errors."""
    pass

class QueryError(DatabaseError):
    """Exception for query-related errors."""
    pass

class ConnectionPool:
    """A simple connection pool for SQLite connections."""
    
    def __init__(self, db_path: str, max_connections: int = 5):
        """Initialize the connection pool."""
        self.db_path = db_path
        self.max_connections = max_connections
        self.connections: queue.Queue = queue.Queue(maxsize=max_connections)
        self.lock = threading.Lock()
        self._fill_pool()
        
    def _fill_pool(self) -> None:
        """Fill the connection pool up to max_connections."""
        for _ in range(self.max_connections):
            conn = sqlite3.connect(
                self.db_path,
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
            )
            conn.row_factory = sqlite3.Row
            self.connections.put(conn)
            
    def get_connection(self) -> sqlite3.Connection:
        """Get a connection from the pool."""
        try:
            return self.connections.get(timeout=5)
        except queue.Empty:
            raise ConnectionError("No available database connections")
            
    def return_connection(self, conn: sqlite3.Connection) -> None:
        """Return a connection to the pool."""
        self.connections.put(conn)
        
    def close_all(self) -> None:
        """Close all connections in the pool."""
        while not self.connections.empty():
            conn = self.connections.get()
            conn.close()

class BaseDB:
    """Base class for database operations with enhanced functionality."""
    
    def __init__(
        self,
        db_path: str = "vortex.db",
        max_connections: int = 5,
        enable_foreign_keys: bool = True
    ):
        """Initialize database with connection pool."""
        self.db_path = db_path
        self._ensure_db_exists()
        self.pool = ConnectionPool(db_path, max_connections)
        self.enable_foreign_keys = enable_foreign_keys
        self.logger = logging.getLogger(__name__)
        
    def _ensure_db_exists(self) -> None:
        """Ensure database and required tables exist."""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        with self._get_connection() as conn:
            if self.enable_foreign_keys:
                conn.execute("PRAGMA foreign_keys = ON")
            self._create_tables(conn)
            
    @contextmanager
    def _get_connection(self) -> sqlite3.Connection:
        """Context manager for getting a connection from the pool."""
        conn = self.pool.get_connection()
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            raise
        finally:
            self.pool.return_connection(conn)
            
    @contextmanager
    def transaction(self) -> sqlite3.Connection:
        """Context manager for transaction handling."""
        with self._get_connection() as conn:
            try:
                yield conn
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise QueryError(f"Transaction failed: {str(e)}")
            
    def _create_tables(self, conn: sqlite3.Connection) -> None:
        """Create necessary database tables if they don't exist."""
        # Base tables for core functionality
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                version INTEGER DEFAULT 1
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP,
                metadata TEXT,
                session_type TEXT,
                status TEXT DEFAULT 'active',
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                session_id TEXT,
                event_type TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data TEXT,
                severity TEXT DEFAULT 'info',
                processed BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            )
        """)
        
        # Create indices for better query performance
        conn.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_events_session_id ON events(session_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type)")
        
    def execute(
        self,
        query: str,
        params: Union[tuple, Dict[str, Any]] = (),
        fetch_all: bool = True
    ) -> List[Dict[str, Any]]:
        """Execute a SQL query with enhanced error handling."""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(query, params)
                if fetch_all:
                    return [dict(row) for row in cursor.fetchall()]
                result = cursor.fetchone()
                return [dict(result)] if result else []
        except sqlite3.Error as e:
            self.logger.error(f"Query execution failed: {str(e)}")
            raise QueryError(f"Query execution failed: {str(e)}")
            
    def insert(
        self,
        table: str,
        data: Dict[str, Any],
        return_id: bool = True
    ) -> Union[str, int]:
        """Insert a record with better error handling and return options."""
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            with self.transaction() as conn:
                cursor = conn.execute(query, tuple(data.values()))
                return cursor.lastrowid if return_id else cursor.rowcount
        except sqlite3.Error as e:
            self.logger.error(f"Insert operation failed: {str(e)}")
            raise QueryError(f"Insert operation failed: {str(e)}")
            
    def update(
        self,
        table: str,
        data: Dict[str, Any],
        where: Dict[str, Any],
        return_affected: bool = False
    ) -> Union[bool, int]:
        """Update records with enhanced functionality."""
        try:
            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            where_clause = ' AND '.join([f"{k} = ?" for k in where.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            
            with self.transaction() as conn:
                cursor = conn.execute(
                    query,
                    tuple(data.values()) + tuple(where.values())
                )
                return cursor.rowcount if return_affected else cursor.rowcount > 0
        except sqlite3.Error as e:
            self.logger.error(f"Update operation failed: {str(e)}")
            raise QueryError(f"Update operation failed: {str(e)}")
            
    def delete(
        self,
        table: str,
        where: Dict[str, Any],
        return_affected: bool = False
    ) -> Union[bool, int]:
        """Delete records with enhanced functionality."""
        try:
            where_clause = ' AND '.join([f"{k} = ?" for k in where.keys()])
            query = f"DELETE FROM {table} WHERE {where_clause}"
            
            with self.transaction() as conn:
                cursor = conn.execute(query, tuple(where.values()))
                return cursor.rowcount if return_affected else cursor.rowcount > 0
        except sqlite3.Error as e:
            self.logger.error(f"Delete operation failed: {str(e)}")
            raise QueryError(f"Delete operation failed: {str(e)}")
            
    def get_by_id(
        self,
        table: str,
        id_value: str,
        columns: Optional[List[str]] = None
    ) -> Optional[Dict[str, Any]]:
        """Get a record by its ID with column selection."""
        cols = ', '.join(columns) if columns else '*'
        query = f"SELECT {cols} FROM {table} WHERE id = ?"
        results = self.execute(query, (id_value,))
        return results[0] if results else None
        
    def serialize_metadata(self, metadata: Dict[str, Any]) -> str:
        """Serialize metadata dictionary to JSON string."""
        try:
            return json.dumps(metadata, default=str)
        except (TypeError, ValueError) as e:
            self.logger.error(f"Metadata serialization failed: {str(e)}")
            raise ValueError(f"Failed to serialize metadata: {str(e)}")
        
    def deserialize_metadata(self, metadata_str: str) -> Dict[str, Any]:
        """Deserialize JSON string to metadata dictionary."""
        if not metadata_str:
            return {}
        try:
            return json.loads(metadata_str)
        except json.JSONDecodeError as e:
            self.logger.error(f"Metadata deserialization failed: {str(e)}")
            raise ValueError(f"Failed to deserialize metadata: {str(e)}")
            
    def __del__(self):
        """Cleanup connections when object is destroyed."""
        if hasattr(self, 'pool'):
            self.pool.close_all() 