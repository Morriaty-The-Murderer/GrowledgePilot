from controllers.objective_controller import ObjectiveController
from controllers.user_controller import UserController
from ui_pages.home_page import HomePage
from ui_pages.learning_page import LearningPage
from utils.database import init_db, SessionLocal

if __name__ == "__main__":
    init_db()
    db = SessionLocal()

    # Initialize controllers
    user_controller = UserController(db)
    objective_controller = ObjectiveController(db)

    # Create test data if not exists
    test_user = user_controller.get_user(1)
    if not test_user:
        # Create test user with learning preferences
        user = user_controller.create_user(
            name="Test User",
            age=30,
            occupation="Software Engineer",
            language_preference="English"
        )

        # Initialize meta prompt session
        user_controller.start_meta_prompt_flow(user.id)

        # Create test objectives
        objective_controller.create_objective(
            user_id=user.id,
            name="Spanish",
            description="Learn Spanish for travel and communication.",
            priority=1,
            current_level="Beginner",
            target_level="Intermediate"
        )

        objective_controller.create_objective(
            user_id=user.id,
            name="Investment",
            description="Learn about stock market investment.",
            priority=2,
            current_level="Beginner",
            target_level="Intermediate"
        )

    try:
        # Initialize pages
        learning_page = LearningPage(db=db)
        home_page = HomePage(db=db, learning_page=learning_page)

        # Launch the application
        home_page.launch()
    finally:
        # Ensure database session is closed
        db.close()
