import eventmanager
import model
import view
import controller

def run():
    event_manager = eventmanager.EventManager()
    game_model = model.GameEngine(event_manager)
    keyboard = controller.Keyboard(event_manager, game_model)
    graphics = view.GraphicalView(event_manager, game_model)
    game_model.run()

if __name__ == '__main__':
    run()
