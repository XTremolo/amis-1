create or replace package groupPackage IS
    PROCEDURE GROUPCREATEPROC(group_name IN VARCHAR2, user_id IN NUMBER);
end groupPackage;

create or replace package body groupPackage IS
    Procedure GROUPCREATEPROC(group_name IN VARCHAR2, user_id IN NUMBER) IS
    begin
        INSERT INTO BOOK_GROUP(NAME, OWNER_ID) values(group_name, user_id);
    end GROUPCREATEPROC;
END groupPackage;

create or replace package bookGroupPackage IS
    Procedure deleteBookFromGroupPROC(group_id IN NUMBER, book_id IN NUMBER, user_id IN NUMBER);
end bookGroupPackage;

create or replace package body bookGroupPackage IS
    Procedure deleteBookFromGroupPROC(group_id IN NUMBER, 
        book_id IN NUMBER, user_id IN NUMBER) IS
    begin
        DELETE FROM BOOK_GROUP_BOOKS WHERE BOOK_ID = book_id;
    end;
end bookGroupPackage;

begin
bookGroupPackage.deleteBookFromGroupPROC(4, 0);
end;