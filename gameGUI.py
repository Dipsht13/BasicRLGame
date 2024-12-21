
import sys
import customtkinter as ctk
from PIL import Image, ImageTk

import game_engine as game

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class MessageBox(ctk.CTkToplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x200")
        self.grab_set()  # Focus on this window

        # Message Label
        self.message_label = ctk.CTkLabel(self, text=message, wraplength=350)
        self.message_label.pack(pady=20, padx=20)

        # OK Button
        self.ok_button = ctk.CTkButton(self, text="Fuck Off", command=self.on_close)
        self.ok_button.pack(pady=10)

    def on_close(self):
        self.destroy()
        
class GameOverBox(ctk.CTkToplevel):
    def __init__(self, parent, message):
        super().__init__(parent)
        self.title('Game Over')
        self.geometry("400x200")
        self.grab_set()
        
        self.message_label = ctk.CTkLabel(self, text= message, wraplength=350)
        self.message_label.pack(pady=20, padx=20)
        
        #ok button
        self.ok_button = ctk.CTkButton(self, text= "Ok", command=self.on_close)
        self.ok_button.pack(pady=10)
        
    def on_close(self):
        self.destroy()


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        
        #initialize game
        self.player, self.enemy = game.Initialize()
        game.NewTurn(self.player, self.enemy)

        # configure window
        self.title("Trash the Tower v0.1")
        self.geometry("900x630")
        self.resizable(False, False)

        # create frame
        self.frame = ctk.CTkFrame(master=self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # create canvases
        self.playerCanvas = ctk.CTkCanvas(self.frame, width=300, height=400)
        self.playerCanvas.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        self.enemyCanvas = ctk.CTkCanvas(self.frame, width=300, height=200)
        self.enemyCanvas.grid(row=0, column=1, sticky="e", padx=10, pady=10)
        
        self.load_images()

        # create player status textbox
        self.playerText = ctk.CTkTextbox(master = self.frame)
        self.playerText.grid(row=1, column=0, sticky = 'nsew')
        
        # create enemy status textbox
        self.enemyText = ctk.CTkTextbox(master = self.frame)
        self.enemyText.grid(row=1, column=1, sticky = 'nsew')

        # create main textbox
        self.textbox = ctk.CTkTextbox(master=self.frame)
        self.textbox.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # create button frame
        self.button_frame = ctk.CTkFrame(master=self)
        self.button_frame.grid(row=1, column=0, sticky="ew")

        # create buttons
        self.update_card_buttons()

        # configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Configure rows for self.frame
        self.frame.grid_rowconfigure(0, minsize=400, weight=0)  # Images - Fixed height
        self.frame.grid_rowconfigure(1, weight=2)  # Player & Enemy textboxes - Fixed height
        self.frame.grid_rowconfigure(2, weight=1)  # Main textbox - Expandable
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        
        # populate text box
        self.update_text_boxes()

    
    def load_images(self):
        # Load and resize images
        playerImg = Image.open(self.player.image).resize((300, 500))
        enemyImg = Image.open(self.enemy.image).resize((300, 200))
    
        # Convert to PhotoImage
        self.playerPhoto = ImageTk.PhotoImage(playerImg)
        self.enemyPhoto = ImageTk.PhotoImage(enemyImg)
    
        # Display images
        self.playerCanvas.create_image(0, 0, anchor="nw", image=self.playerPhoto)
        self.enemyCanvas.create_image(0, 0, anchor="nw", image=self.enemyPhoto)



    def update_text_boxes(self):
        
        self.playerState = game.StatusReport(self.player)
        self.playerText.delete("1.0", "end")
        self.playerText.insert("1.0", self.playerState)
        
        self.enemyState = game.StatusReport(self.enemy)
        self.enemyText.delete("1.0", "end")
        self.enemyText.insert("1.5", self.enemyState)
        
        self.gameState = game.UpdateGameState(self.player, self.enemy)
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", self.gameState)
        

    def update_card_buttons(self):
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        self.button_frame.update_idletasks()
    
        # Create new buttons
        for idx, card in enumerate(self.player.hand):
            button = ctk.CTkButton(
                master=self.button_frame,
                text=f"{card.displayStr}\n ({card.mana} mana)",
                width=60, height=60,
                corner_radius=8,
                command=lambda i=idx: self.click_on_card(i)
            )
            button.grid(row=0, column=idx, padx=10, pady=10)
        endTurn = ctk.CTkButton(master = self.button_frame, text = "End Turn",
                                width = 80, height = 40, corner_radius = 6, 
                                command = self.click_on_end_turn)
        endTurn.grid(row=0, column=idx+1, padx=10, pady=10)
        
        
    def click_on_card(self, cardix):
        
        successful, errorMsg = game.PlayCard(self.player, self.enemy, cardix)
        
        if not successful:
            MessageBox(self, "Sorry bro", errorMsg)
        
        else:
            self.update_text_boxes()
            self.update_card_buttons()
        
            
    def click_on_end_turn(self):
        
        self.gameOver = game.EndTurn(self.player, self.enemy)
        if self.gameOver:
            self.update_text_boxes()
            goBox = GameOverBox(self, self.gameState)
            self.wait_window(goBox)
            self.destroy()
            
        else:
            game.NewTurn(self.player, self.enemy)
            self.update_text_boxes()
            self.update_card_buttons()
            

if __name__ == "__main__":
    app = App()
    app.mainloop()