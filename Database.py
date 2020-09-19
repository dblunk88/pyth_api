from sqlalchemy import Column,Integer,ForeignKey,String,ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Questions(Base):
    __tablename__ = 'questions'
    __table_args__ = {'extend_existing': True}
    questions_id = Column(Integer,primary_key=True)
    question = Column(String,nullable=False)


class Answer_Type(Base):
    __tablename__ = 'answer_type'
    __table_args__ = {'extend_existing': True}
    answer_type_id = Column(Integer,primary_key=True)
    answer_type = Column(String,nullable=False)
    label = Column(String)


class Assessment(Base):
    __tablename__ = 'assessment'
    __table_args__ = {'extend_existing': True}
    assessment_id = Column(Integer,primary_key=True)
    title = Column(String)
    description = Column(String)
    category = Column(String)


class Question_Answer(Base):
    __tablename__ = 'questions_answer'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer,primary_key=True)
    question_id = Column(Integer,ForeignKey("Questions.questions_id"))
    answer_type_id = Column(Integer,ForeignKey("Answer_type.answer_type_id"))


class Results(Base):
    __tablename__ = 'results'
    __table_args__ = {'extend_existing': True}
    results_id = Column(Integer,primary_key=True)
    parent_company = Column(String)
    value = Column(Integer)
    answer_type_id = Column(Integer,ForeignKey("answer_type.answer_type_id"))
    user_id = Column(Integer,ForeignKey("users.user_id"))
    category = Column(String)
    assessment_id = Column(Integer,ForeignKey("assessment.assessment_id"))


class User_Type(Base):
    __tablename__ = 'user_type'
    __table_args__ = {'extend_existing': True}
    user_type_id = Column(Integer,primary_key=True)
    type = Column(String)


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    user_id = Column(Integer,primary_key=True)
    username = Column(String)
    uid = Column(String)
    user_type_id = Column(Integer,ForeignKey("user_type.user_type_id"))
    completed_forms = Column(ARRAY(Integer))
    pending_forms = Column(ARRAY(Integer))
    company_id = Column(Integer,ForeignKey("companies.company_id"))
    email = Column(String)
    img_url = Column(String)


class Forms(Base):
    __tablename__ = 'forms'
    __table_args__ = {'extend_existing': True}
    form_id = Column(Integer,primary_key=True)
    # question_ids = Column(ARRAY(Integer))
    form_title = Column(String)


class Companies(Base):
    __tablename__ = 'companies'
    __table_args__ = {'extend_existing': True}
    company_id = Column(Integer,primary_key=True)
    company_name = Column(String)
    img_url = Column(String)
