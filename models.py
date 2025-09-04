from sqlalchemy import Column, Integer, String, Date, Float, Boolean, ForeignKey, Text, DateTime,Enum as SQLAEnum
import datetime
import enum
from sqlalchemy.orm import relationship, declarative_base
from enum import Enum


class ChildTypeEnum(enum.Enum):
    FULL_DAY = "اليوم الكامل"
    SESSIONS = "جلسات"

Base = declarative_base()

# -------------------------------
# Users and Roles
# -------------------------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50))  # e.g. admin, trainer, accountant

    # One user can manage many children (if trainer)
    children = relationship("Child", back_populates="created_by")


# -------------------------------
# Children Table
# -------------------------------
class Child(Base):
    __tablename__ = "children"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=False)
    age = Column(Integer)
    phone_number = Column(String(20))
    father_job = Column(String(100))
    mother_job = Column(String(100))
    notes = Column(String(225))
    problems = Column(String(255))
    child_image = Column(String(255))  # path to the child's image
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    child_type = Column(SQLAEnum(ChildTypeEnum), default=ChildTypeEnum.FULL_DAY)
    is_deleted = Column(Boolean, default=False)
    has_left = Column(Boolean, default=False)


    # Relation to user who added the child
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_by = relationship("User", back_populates="children")

    # One-to-one: child can have one full-day program
    full_day_program = relationship("FullDayProgram", back_populates="child", uselist=False)

    # One-to-many: child can have multiple individual sessions
    individual_sessions = relationship("IndividualSession", back_populates="child")

    # One-to-many: daily visits
    daily_visits = relationship("DailyVisit", back_populates="child")

    # One-to-many: daily finances
    daily_finances = relationship("DailyFinance", back_populates="child")


# -------------------------------
# Full Day Program
# -------------------------------
class FullDayProgram(Base):
    __tablename__ = "full_day_programs"
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)

    entry_date = Column(Date, nullable=False)                         # تاريخ الدخول
    diagnosis = Column(String(500))                                   # التشخيص

    monthly_fee = Column(Float)                                       # قيمة الاشتراك الشهري
    bus_fee = Column(Float)                                           # قيمة اشتراك الباص

    personal_photo = Column(String(255), nullable=True)               # صورة شخصية (مسار/رابط)
    birth_certificate = Column(String(255), nullable=True)            # شهادة الميلاد
    father_id_card = Column(String(255), nullable=True)               # بطاقة الأب
    test_documents = Column(String(255), nullable=True)               # ملفات أو صور للاختبارات

    tests_applied_file = Column(String(255), nullable=True)           # ملف الاختبارات المطبقة
    training_plan_file = Column(String(255), nullable=True)           # ملف الخطة التدريبية
    monthly_report_file = Column(String(255), nullable=True)          # ملف التقرير الشهري
    child_documents_file = Column(String(255), nullable=True)         # ملف الأوراق الخاصة بالطفل (لو مجمعينها في ملف واحد)

    notes = Column(String(1000))                                      # ملاحظات إضافية
    attendance_status = Column(String(50))                            # Regular / Irregular

    child = relationship("Child", back_populates="full_day_program")


# -------------------------------
# Individual Sessions
# -------------------------------
class IndividualSession(Base):
    __tablename__ = "individual_sessions"

    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)

    entry_date = Column(Date, nullable=False)
    diagnosis = Column(String(500))  # التشخيص
    tests_applied_file = Column(String(255))  # ملفات الاختبارات المطبقة
    session_fee = Column(Float)
    monthly_sessions_count = Column(Integer)
    attended_sessions_count = Column(Integer)
    specialist_name = Column(String(100))
    monthly_report_file = Column(String(255))  # ملفات التقرير الشهري

    
    personal_photo = Column(String(255), nullable=True)        # صورة شخصية
    birth_certificate = Column(String(255), nullable=True)     # شهادة الميلاد
    father_id_card = Column(String(255), nullable=True)        # بطاقة الأب
    child_documents_file = Column(String(255), nullable=True)  # أي أوراق إضافية

    notes = Column(String(1000))  

    child = relationship("Child", back_populates="individual_sessions")


# -------------------------------
# Daily Visits
# -------------------------------
class DailyVisit(Base):
    __tablename__ = "daily_visits"
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey("children.id"))
    value = Column(Float)
    appointment = Column(String(50))
    date = Column(Date)
    purpose = Column(Text)
    notes = Column(Text)

    child = relationship("Child", back_populates="daily_visits")


# -------------------------------
# Daily Finance
# -------------------------------
class DailyFinance(Base):
    __tablename__ = "daily_finances"
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey("children.id"))
    value = Column(Float)
    remaining = Column(Float)
    count = Column(Integer)
    service = Column(String(50))  # FullDay / Individual
    payment_date = Column(Date)
    notes = Column(Text)

    child = relationship("Child", back_populates="daily_finances")


# -------------------------------
# Monthly Finance - Full Day
# -------------------------------
class MonthlyFinanceFullDay(Base):
    __tablename__ = "monthly_finance_full_day"
    id = Column(Integer, primary_key=True)
    month = Column(String(20))
    total_income = Column(Float)
    rent = Column(Float)
    transport = Column(Float)
    loans = Column(Float)
    salaries = Column(Float)
    monthly_expenses = Column(Float)
    external_remaining = Column(Float)
    remaining = Column(Float)
    notes = Column(Text)


# -------------------------------
# Monthly Finance - Individual Sessions
# -------------------------------
class MonthlyFinanceIndividual(Base):
    __tablename__ = "monthly_finance_individual"
    id = Column(Integer, primary_key=True)
    month = Column(String(20))
    total_income = Column(Float)
    specialists_total = Column(Float)
    center_total = Column(Float)
    loans = Column(Float)
    specialists_details = Column(Text)  # JSON or text format (name, value)
    external_remaining = Column(Float)
    remaining = Column(Float)
    notes = Column(Text)


# -------------------------------
# Monthly Finance - Overall
# -------------------------------
class MonthlyFinanceOverall(Base):
    __tablename__ = "monthly_finance_overall"
    id = Column(Integer, primary_key=True)
    month = Column(String(20))
    full_day_income = Column(Float)
    individual_income = Column(Float)
    full_day_expenses = Column(Float)
    individual_expenses = Column(Float)
    external_remaining_full_day = Column(Float)
    external_remaining_individual = Column(Float)
    loans = Column(Float)
    current_total = Column(Float)
    notes = Column(Text)


# -------------------------------
# Tools Inventory (Center-owned)
# -------------------------------
class TrainingTool(Base):
    __tablename__ = "training_tools"
    id = Column(Integer, primary_key=True)
    tool_name = Column(String(100))
    tool_number = Column(String(50))
    tool_image = Column(String(255))  # path to image
    department = Column(String(100))
    purchase_date = Column(Date)
    notes = Column(String (1000))


# -------------------------------
# Tools for Sale
# -------------------------------
class ToolForSale(Base):
    __tablename__ = "tools_for_sale"
    id = Column(Integer, primary_key=True)
    tool_name = Column(String(100))
    quantity = Column(Integer)
    buy_price = Column(Float)
    sell_price = Column(Float)
    tool_number = Column(String(50))
    remaining = Column(Integer)
    notes = Column(String(1000))


# -------------------------------
# Uniforms for Sale
# -------------------------------
class UniformForSale(Base):
    __tablename__ = "uniforms_for_sale"
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    buy_price = Column(Float)
    sell_price = Column(Float)
    remaining = Column(Integer)
    notes = Column(String(1000))


# -------------------------------
# Books for Sale
# -------------------------------
class BookForSale(Base):
    __tablename__ = "books_for_sale"
    id = Column(Integer, primary_key=True)
    book_name = Column(String(100))
    quantity = Column(Integer)
    buy_price = Column(Float)
    sell_price = Column(Float)
    remaining = Column(Integer)
    notes = Column(String(1000))
