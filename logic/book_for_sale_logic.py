from sqlalchemy.orm import Session
from models import BookForSale
from DTOs.book_for_sale_dto import BookForSaleDTO, CreateBookForSaleDTO
from mapper import map_to_dto, map_to_model, update_model_from_dto


class BookForSaleService:
    @staticmethod
    def create_book(db: Session, book_data: CreateBookForSaleDTO) -> BookForSaleDTO:
        book = map_to_model(book_data, BookForSale)
        db.add(book)
        db.commit()
        db.refresh(book)
        return map_to_dto(book, BookForSaleDTO)

    @staticmethod
    def get_book(db: Session, book_id: int) -> BookForSaleDTO | None:
        book = db.query(BookForSale).filter(BookForSale.id == book_id).first()
        return map_to_dto(book, BookForSaleDTO) if book else None

    @staticmethod
    def get_all_books(db: Session) -> list[BookForSaleDTO]:
        books = db.query(BookForSale).all()
        return [map_to_dto(b, BookForSaleDTO) for b in books]

    @staticmethod
    def update_book(
        db: Session, book_id: int, book_data: CreateBookForSaleDTO
    ) -> BookForSaleDTO | None:
        book = db.query(BookForSale).filter(BookForSale.id == book_id).first()
        if not book:
            return None
        book = update_model_from_dto(book, book_data)
        db.commit()
        db.refresh(book)
        return map_to_dto(book, BookForSaleDTO)

    @staticmethod
    def delete_book(db: Session, book_id: int) -> bool:
        book = db.query(BookForSale).filter(BookForSale.id == book_id).first()
        if not book:
            return False
        db.delete(book)
        db.commit()
        return True
