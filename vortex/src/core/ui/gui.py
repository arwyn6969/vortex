"""
Modern GUI implementation for the Vortex of Enlightenment using customtkinter.
"""
import customtkinter as ctk
from typing import Optional, Callable, List, Dict
from datetime import datetime
import threading
from PIL import Image, ImageTk

class VortexGUI:
    """Modern GUI implementation for Vortex of Enlightenment."""
    
    def __init__(self):
        """Initialize the GUI window and components."""
        # Set the appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create the main window
        self.window = ctk.CTk()
        self.window.title("Vortex of Enlightenment")
        self.window.geometry("1200x800")
        
        # Configure grid layout
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        
        # Create main components
        self._create_header()
        self._create_main_display()
        self._create_quick_response_buttons()
        self._create_chat_interface()
        self._create_stats_overview()
        
        # Initialize callbacks
        self.message_callback: Optional[Callable[[str], None]] = None
        self.button_callback: Optional[Callable[[str], None]] = None
    
    def _create_header(self):
        """Create the header section with title and stats overview."""
        header_frame = ctk.CTkFrame(self.window)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        title = ctk.CTkLabel(
            header_frame,
            text="Vortex of Enlightenment",
            font=("Helvetica", 24, "bold")
        )
        title.pack(side="left", padx=10)
        
        # Stats button that will show the dashboard
        self.stats_button = ctk.CTkButton(
            header_frame,
            text="Dashboard",
            command=self._show_dashboard
        )
        self.stats_button.pack(side="right", padx=10)
    
    def _create_main_display(self):
        """Create the main display area for messages and images."""
        self.display_frame = ctk.CTkFrame(self.window)
        self.display_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        self.display_frame.grid_columnconfigure(0, weight=1)
        self.display_frame.grid_rowconfigure(0, weight=1)
        
        # Create scrollable text area
        self.display_text = ctk.CTkTextbox(
            self.display_frame,
            wrap="word",
            font=("Helvetica", 12)
        )
        self.display_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.display_text.configure(state="disabled")
    
    def _create_quick_response_buttons(self):
        """Create the 2x2 grid of quick response buttons."""
        button_frame = ctk.CTkFrame(self.window)
        button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        # Configure grid layout for 2x2 buttons
        for i in range(2):
            button_frame.grid_columnconfigure(i, weight=1)
        
        self.quick_buttons: List[ctk.CTkButton] = []
        default_responses = ["Yes", "No", "Tell me more", "Go back"]
        
        for i in range(2):
            for j in range(2):
                idx = i * 2 + j
                button = ctk.CTkButton(
                    button_frame,
                    text=default_responses[idx],
                    command=lambda x=default_responses[idx]: self._handle_quick_response(x)
                )
                button.grid(row=i, column=j, padx=5, pady=5, sticky="ew")
                self.quick_buttons.append(button)
    
    def _create_chat_interface(self):
        """Create the chat interface with input field and send button."""
        chat_frame = ctk.CTkFrame(self.window)
        chat_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        
        chat_frame.grid_columnconfigure(0, weight=1)
        
        # Create input field
        self.input_field = ctk.CTkEntry(
            chat_frame,
            placeholder_text="Type your message here..."
        )
        self.input_field.grid(row=0, column=0, sticky="ew", padx=(5, 2), pady=5)
        
        # Create send button
        self.send_button = ctk.CTkButton(
            chat_frame,
            text="Send",
            command=self._handle_send
        )
        self.send_button.grid(row=0, column=1, padx=(2, 5), pady=5)
        
        # Bind Enter key to send
        self.input_field.bind("<Return>", lambda event: self._handle_send())
    
    def _create_stats_overview(self):
        """Create the stats overview panel."""
        self.stats_frame = ctk.CTkFrame(self.window)
        self.stats = {}
        
        # Initialize with placeholder stats
        self._update_stats({
            "Level": "1",
            "Experience": "0/100",
            "Wisdom": "10",
            "Progress": "0%"
        })
    
    def _update_stats(self, stats_dict: Dict[str, str]):
        """Update the stats display with new values."""
        for key, value in stats_dict.items():
            if key not in self.stats:
                label = ctk.CTkLabel(
                    self.stats_frame,
                    text=f"{key}: {value}",
                    font=("Helvetica", 12)
                )
                label.pack(side="left", padx=10)
                self.stats[key] = label
            else:
                self.stats[key].configure(text=f"{key}: {value}")
    
    def _handle_send(self):
        """Handle sending a message from the chat interface."""
        message = self.input_field.get().strip()
        if message and self.message_callback:
            self.message_callback(message)
            self.input_field.delete(0, "end")
    
    def _handle_quick_response(self, response: str):
        """Handle quick response button clicks."""
        if self.button_callback:
            self.button_callback(response)
    
    def _show_dashboard(self):
        """Show the detailed dashboard (placeholder for now)."""
        dashboard = ctk.CTkToplevel(self.window)
        dashboard.title("Vortex Dashboard")
        dashboard.geometry("800x600")
        
        # Placeholder for dashboard content
        label = ctk.CTkLabel(
            dashboard,
            text="Dashboard content coming soon...",
            font=("Helvetica", 16)
        )
        label.pack(expand=True)
    
    def display_message(self, message: str, message_type: str = "system"):
        """Display a message in the main display area."""
        self.display_text.configure(state="normal")
        timestamp = datetime.now().strftime("%H:%M")
        
        # Format based on message type
        if message_type == "user":
            prefix = f"[{timestamp}] You: "
        elif message_type == "system":
            prefix = f"[{timestamp}] System: "
        else:
            prefix = f"[{timestamp}] "
        
        self.display_text.insert("end", prefix + message + "\n")
        self.display_text.configure(state="disabled")
        self.display_text.see("end")
    
    def set_message_callback(self, callback: Callable[[str], None]):
        """Set the callback for handling messages."""
        self.message_callback = callback
    
    def set_button_callback(self, callback: Callable[[str], None]):
        """Set the callback for handling button clicks."""
        self.button_callback = callback
    
    def update_quick_responses(self, responses: List[str]):
        """Update the quick response buttons with new text."""
        for button, text in zip(self.quick_buttons, responses):
            button.configure(text=text)
    
    def start(self):
        """Start the GUI main loop."""
        self.window.mainloop()
    
    def stop(self):
        """Stop the GUI."""
        self.window.quit() 