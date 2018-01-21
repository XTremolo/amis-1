create or replace package groupPackage IS
    PROCEDURE GROUPCREATEPROC(group_name IN VARCHAR2, user_id IN NUMBER);
    PROCEDURE GROUPDELETEPROC(gid IN NUMBER);
    PROCEDURE GROUPEDITPROC(gid IN NUMBER, new_name IN VARCHAR2);
end groupPackage;
/
Commit;

create or replace package body groupPackage IS
    Procedure GROUPCREATEPROC(group_name IN VARCHAR2, user_id IN NUMBER) IS
    begin
        INSERT INTO BOOK_GROUP(NAME, OWNER_ID) values(group_name, user_id);
    end GROUPCREATEPROC;
    Procedure groupdeleteproc(gid IN NUMBER) is
    begin
        Delete from BOOK_GROUP_BOOKS where GROUP_ID = gid;
        Delete from BOOK_GROUP where "ID" = gid;
    end;
    Procedure groupeditproc(gid IN NUMBER, new_name IN VARCHAR2) is
    begin
        UPDATE BOOK_GROUP
          SET NAME = new_name
          WHERE ID = gid;
    end;
END groupPackage;
--
--create or replace package bookGroupPackage IS
--    Procedure deleteBookFromGroupPROC(bid IN NUMBER, gid IN NUMBER);
--end bookGroupPackage;
--
--create or replace package body bookGroupPackage IS
--    Procedure deleteBookFromGroupPROC(bid IN NUMBER, 
--        gid IN NUMBER) AS
--    begin
--        DELETE BOOK_GROUP_BOOKS WHERE "BOOK_ID" = bid AND "GROUP_ID" = gid;
--    end;
--end bookGroupPackage;

--begin
--bookGroupPackage.deleteBookFromGroupPROC(4, 0, 0);
--end;