from sqlalchemy import select, insert, func

from database import session_maker, User, Question, questions_asked_table


async def _get_user_with_questions_and_total_asked(
        user_id: int,
    ) -> tuple[User | None, list[tuple[Question, int]] | None]:

    async with session_maker.begin() as session:
        query_result = (await session.execute(
            select(User, Question).
            where(User.id == user_id).
            join(User.questions_asked)
        )).all()
        if not query_result:
            return None, None
        
        questions_with_total_asked = []
        for u, q in query_result:
            questions_with_total_asked.append([q, await count_times_question_asked(q)])
        
        return u, questions_with_total_asked


async def get_user_by_id(
        id: int,
        *,
        include_questions: bool = False,
    ) -> User | None | tuple[User | None, list[tuple[Question, int]] | None]:
    
    async with session_maker.begin() as session:
        if not include_questions:
            return await session.scalar(
                select(User).
                where(User.id == id)
            )
        
        user = await session.scalar(
            select(User).
            where(User.id == id)
        )
        if user is None:
            return None, None
        
        new_user, questions = await _get_user_with_questions_and_total_asked(user.id)
        return (new_user, questions) if new_user is not None else (user, None)

async def get_user_by_email(
        email: str,
        *,
        include_questions: bool = False,
    ) -> User | None | tuple[User | None, list[tuple[Question, int]] | None]:
    
    async with session_maker.begin() as session:
        if not include_questions:
            return await session.scalar(
                select(User).
                where(User.email == email)
            )
        
        user = await session.scalar(
            select(User).
            where(User.email == email)
        )
        if user is None:
            return None, None
        
        new_user, questions = await _get_user_with_questions_and_total_asked(user.id)
        return (new_user, questions) if new_user is not None else (user, None)


async def create_user(email: str) -> User:
    user = User(email=email)
    async with session_maker.begin() as session:
        session.add(user)
    return user


async def add_question_to_user(user: User, text: str) -> Question:
    async with session_maker.begin() as session:
        question = await session.scalar(
            select(Question).
            where(Question.text == text.lower()) 
        )
        
        if question is None:
            question = Question(
                text = text.lower(),
                users_asked = [user],
            )
            session.add(question)
            return question
        
        # if question exists but relation with it and user is not then create it
        if await session.scalar(
                select(questions_asked_table).
                where(questions_asked_table.c.user_id == user.id).
                where(questions_asked_table.c.question_id == question.id)
            ) is None:
            await session.execute(
                insert(questions_asked_table).
                values(
                    user_id = user.id,
                    question_id = question.id,
                )
            )
        
        return question

async def count_times_question_asked(q: Question) -> int:
    async with session_maker.begin() as session:
        return await session.scalar(
            select(func.count(questions_asked_table.c.question_id)).
            group_by(questions_asked_table.c.question_id).
            having(questions_asked_table.c.question_id == q.id)
        )
