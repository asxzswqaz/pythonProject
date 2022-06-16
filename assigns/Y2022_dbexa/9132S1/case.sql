create table REDLIST_STATUS(
REDLIST_CODE char(2) primary key,
REDLIST_CATEGORY VARCHAR(40)
);

create table SPECIES(
SPEC_GENUS varchar(20),
SPEC_NAME varchar(20),
SPEC_POPULAR_NAME varchar(40),
SPEC_FAMILY varchar(20),
SPEC_NATURAL_RANGE varchar(100),
SPEC_REDLIST_URL varchar(80),
REDLIST_CODE char(2),
primary key (SPEC_GENUS, SPEC_NAME),
foreign key (REDLIST_CODE) references REDLIST_STATUS(REDLIST_CODE)
);


create table CENTRE_TYPE(
CT_CODE char(1),
CT_DESCRIPTION varchar(40),
primary key (CT_CODE)
);

create table CENTRE(
CENTRE_ID char(5),
CENTRE_NAME varchar(40),
CENTRE_ADDRESS varchar(100),
CENTRE_DIRECTOR varchar(30),
CENTRE_PHONE_NO varchar(20),
CT_CODE char(1),
PRIMARY KEY (CENTRE_ID),
FOREIGN KEY (CT_CODE) REFERENCES CENTRE_TYPE(CT_CODE)
);

create table BREEDING_EVENT(
BREVENT_ID numeric(6),
BREVENT_DATE date,
CENTRE_ID char(5),
BREVENT_FATHER_ID NUMERIC(6),
BEVENT_MOTHER_ID NUMERIC(6),
primary key (BREVENT_ID),
foreign key (CENTRE_ID) references CENTRE(CENTRE_ID)
);




create table ANIMAL (
    ANIMAL_ID NUMERIC(6),
    ANIMAL_SEX char(1),
    BREVENT_ID numeric(6),
   CENTRE_ID char(5),
   SPEC_GENUS varchar(20),
   SPEC_NAME varchar(20),
   primary key (ANIMAL_ID),
   foreign key (CENTRE_ID) references CENTRE(CENTRE_ID),
   foreign key (SPEC_GENUS,SPEC_NAME) references SPECIES(SPEC_GENUS,SPEC_NAME),
   foreign key (BREVENT_ID) references BREEDING_EVENT(BREVENT_ID)
);

create table EXCHANGE_TYPE (
    ET_CODE char(1),
    ET_DESCRIPTION varchar(40),
    primary key (ET_CODE)
);

create table EXCHANGE(
EXCHANGE_NO NUMERIC(6),
EXCHANGE_DATE date,
EXCHANGE_FROM_CENTRE_ID char(5),
EXCHANGE_TO_CENTRE_ID CHAR(5),
ANIMAL_ID NUMERIC(6),
ET_CODE CHAR(1),
PRIMARY KEY (EXCHANGE_NO),
FOREIGN KEY (EXCHANGE_FROM_CENTRE_ID) REFERENCES CENTRE(CENTRE_ID),
FOREIGN KEY (EXCHANGE_TO_CENTRE_ID) REFERENCES CENTRE(CENTRE_ID),
FOREIGN KEY (ET_CODE) REFERENCES EXCHANGE_TYPE(ET_CODE)
);


CREATE TABLE GRANT_TYPE(
GT_CODE CHAR(1),
GT_DESCRIPTION VARCHAR(40),
PRIMARY KEY (GT_CODE)
);

CREATE TABLE CONSERVATION_AGENCY(
CA_CODE NUMERIC(4),
CA_AGENCY_NAME VARCHAR(50),
CA_HOME_NO VARCHAR(20),
CA_ADDRESS VARCHAR(100),
CA_TYPE CHAR(1),
PRIMARY KEY (CA_CODE)
);

CREATE TABLE GRANTS(
GRANT_ID NUMERIC(5),
GRANT_AMOUNT NUMERIC(10,2),
CA_CODE NUMERIC(4),
CENTRE_ID CHAR(5),
GT_CODE CHAR(1),
PRIMARY KEY (GRANT_ID),
FOREIGN KEY (CA_CODE) REFERENCES CONSERVATION_AGENCY(CA_CODE),
FOREIGN KEY (CENTRE_ID) REFERENCES CENTRE(CENTRE_ID),
FOREIGN KEY (GT_CODE) REFERENCES GRANT_TYPE(GT_CODE)
);