create or replace package groupPackage IS
    PROCEDURE groupCreateProc(group_name IN VARCHAR2, user_id IN NUMBER);
end groupPackage;

create or replace package body groupPackage IS
    Procedure groupCreateProc(group_name IN VARCHAR2, user_id IN NUMBER) IS
    begin
        INSERT INTO BOOK_GROUP(NAME, OWNER_ID) values(group_name, user_id)
    end
END groupPackage;