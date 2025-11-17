import arcade
from game.game import Game

def main():
    print("Select your kitten color:")
    print("1. Black")
    print("2. Default") 
    print("3. Calico")
    print("4. Ace")
    
    choice = input("Enter your choice (1-4): ").strip()
    
    skin_map = {
        "1": "black",
        "2": "default", 
        "3": "calico",
        "4": "ace"
    }
    
    selected_skin = skin_map.get(choice, "black")
    print(f"Selected skin: {selected_skin}")
    
    game = Game(selected_skin)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
