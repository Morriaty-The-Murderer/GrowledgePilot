from controllers.user_controller import get_user
from utils.database import init_db, get_db
from ui_pages.home_page import HomePage
from ui_pages.learning_page import LearningPage

if __name__ == "__main__":
    init_db()
    db = next(get_db())

    #  创建测试数据。实际使用时，应删除此部分。
    from controllers.user_controller import create_user
    from controllers.objective_controller import create_objective

    test_user = get_user(db, 1)
    if not test_user:
        user = create_user(db=db, name="Test User", age=30, occupation="Software Engineer")
        create_objective(db=db, user_id=user.id, name="Spanish",
                         description="Learn Spanish for travel and communication.", priority=1,
                         current_level="Beginner", target_level="Intermediate")
        create_objective(db=db, user_id=user.id, name="Investment", description="Learn about stock market investment.",
                         priority=2, current_level="Beginner", target_level="Intermediate")

    learning_page = LearningPage(db=db)
    home_page = HomePage(db=db, learning_page=learning_page)

    home_page.launch()
