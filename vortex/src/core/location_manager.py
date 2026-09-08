"""
Location management functionality for the VORTEX system.

The graph is the Tree of Life. Placeholder Hub / Grove / Library rooms
remain only as aliases onto Tiferet so old sessions do not fall off the map.
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from ..core.ui.terminal import TerminalUI
from ..core.engine import CoreEngine
from .lattice import Lattice
from ..mythology.correspondences import get_node_by_pond


@dataclass
class Location:
    name: str
    description: str
    connections: List[str]


class LocationManager:
    """Manages navigation along sefirot paths."""

    def __init__(self, ui: TerminalUI, engine: CoreEngine):
        self.ui = ui
        self.engine = engine
        self.lattice = Lattice()
        self.locations: Dict[str, Location] = {}
        self._build_from_lattice()
        self.engine.event_bus.subscribe("location_changed", self._on_location_changed)

    def _build_from_lattice(self) -> None:
        graph = self.lattice.location_graph()
        for pond, exits in graph.items():
            node = get_node_by_pond(pond)
            extra = ""
            if node:
                extra = f" Pillar of {node.pillar}. Office of {node.sefirah}."
                if node.ledger_floor:
                    extra += " The ledger floor. Keys stay in your wallet."
            self.locations[pond] = Location(
                name=pond,
                description=self.lattice.describe(pond) + extra,
                connections=list(exits),
            )
        vibe = "Vibe Temple"
        for alias in ("Central Hub", "Reflection Pool", "Sacred Grove"):
            if vibe in self.locations:
                self.locations[alias] = Location(
                    name=vibe,
                    description=self.locations[vibe].description,
                    connections=self.locations[vibe].connections,
                )

    def get_current_location(self) -> Optional[Location]:
        current = self.engine.get_current_location()
        return self.locations.get(current)

    def get_available_connections(self) -> List[str]:
        location = self.get_current_location()
        return location.connections if location else []

    def can_move_to(self, destination: str) -> bool:
        current = self.engine.get_current_location() or ""
        try:
            return self.lattice.can_travel(current, destination)
        except Exception:
            connections = self.get_available_connections()
            return any(destination.lower() in conn.lower() for conn in connections)

    def move_to(self, destination: str) -> bool:
        current = self.engine.get_current_location() or ""
        try:
            node = self.lattice.travel(current, destination)
        except Exception:
            self.ui.display_text(
                f"There is no stream from here to {destination}. Paths follow the tree."
            )
            return False
        self.engine.set_current_location(node.pond)
        return True

    def show_location_description(self):
        location = self.get_current_location()
        if not location:
            return
        self.ui.display_text(f"\nYou are in the {location.name}")
        self.ui.display_text(f"\n{location.description}")
        if location.connections:
            self.ui.display_text("\nStreams lead to:")
            for conn in location.connections:
                self.ui.display_text(f"  \u2022 {conn}")

    def _on_location_changed(self, data: dict):
        if data and "location" in data:
            self.show_location_description()

    def add_location(self, name: str, description: str, connections: List[str]):
        self.locations[name] = Location(
            name=name,
            description=description,
            connections=connections,
        )
        for conn in connections:
            if conn in self.locations and name not in self.locations[conn].connections:
                self.locations[conn].connections.append(name)

    def remove_location(self, name: str):
        if name in self.locations:
            location = self.locations[name]
            for conn in location.connections:
                if conn in self.locations and name in self.locations[conn].connections:
                    self.locations[conn].connections.remove(name)
            del self.locations[name]
