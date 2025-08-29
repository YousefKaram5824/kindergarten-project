from sqlalchemy.orm import Session
from models import User as UserModel
from database import get_db
import hashlib, secrets

class AuthManager:
    def __init__(self):
        pass  # مش هنخزن users في memory، هنجيبهم من DB عند الحاجة

    def hash_password(self, password, salt=None):
        if salt is None:
            salt = secrets.token_hex(16)
        salted_password = salt + password
        hashed = hashlib.sha256(salted_password.encode()).hexdigest()
        return f"{salt}${hashed}"

    def verify_password(self, stored_password, provided_password):
        try:
            salt, stored_hash = stored_password.split("$")
            salted_password = salt + provided_password
            provided_hash = hashlib.sha256(salted_password.encode()).hexdigest()
            return provided_hash == stored_hash
        except:
            return False

    def create_user(self, db: Session, username, password, role="admin"):
        # check if exists
        existing = db.query(UserModel).filter(UserModel.username == username).first()
        if existing:
            return False, "اسم المستخدم موجود مسبقاً"

        hashed_password = self.hash_password(password)
        new_user = UserModel(username=username, password=hashed_password, role=role)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return True, "تم إنشاء المستخدم بنجاح"

    def authenticate(self, db: Session, username, password):
        user = db.query(UserModel).filter(UserModel.username == username).first()
        if user and self.verify_password(user.password, password):
            return True, user
        return False, "اسم المستخدم أو كلمة المرور غير صحيحة"

    def initialize_default_admin(self, db: Session):
        admin_exists = db.query(UserModel).first()
        if not admin_exists:
            return self.create_user(db, "admin", "admin123", "admin")
        return True, "المستخدمون موجودون بالفعل"

    def reset_password(self, db: Session, username, new_password, admin_username, admin_password):
        # تحقق من هوية الأدمن
        ok, admin_or_msg = self.authenticate(db, admin_username, admin_password)
        if not ok:
            return False, "كلمة مرور المدير غير صحيحة"
        if admin_or_msg.role != "admin":
            return False, "ليست لديك صلاحية لإعادة تعيين كلمات المرور"

        user = db.query(UserModel).filter(UserModel.username == username).first()
        if not user:
            return False, "المستخدم غير موجود"

        user.password = self.hash_password(new_password)
        db.commit()
        return True, "تم إعادة تعيين كلمة المرور بنجاح"

    def verify_admin(self, db: Session, username, password):
        ok, user_or_msg = self.authenticate(db, username, password)
        if not ok:
            return False, user_or_msg
        if user_or_msg.role != "admin":
            return False, "ليست لديك صلاحية المدير"
        return True, "تم التحقق من هوية المدير بنجاح"


# نعمل instance
auth_manager = AuthManager()
