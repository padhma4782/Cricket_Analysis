
import pandas as pd
import mysql.connector

# define student database connections, tables creation and access for them.
class CricketDatabaseManager:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()
    
    def create_table(self, query):
        self.cursor.execute(query)
        self.connection.commit()
    
    def insert_data(self, query, data):
        self.cursor.executemany(query, data)
        self.connection.commit()

    def query(self, query, params=None):
        self.cursor.execute(query, params)
        data = self.cursor.fetchall()
        column_names = [desc[0] for desc in self.cursor.description]
        return column_names,data
    
    def close(self):
        self.cursor.close()
        self.connection.close()

    def DBLoader(self,studentdf,programmingdf,softskilldf,placementdf):

# Creating Students table
        create_students_query = '''
                                CREATE TABLE IF NOT EXISTS Students 
                                (
                                    StudentID VARCHAR(255) PRIMARY KEY,
                                    Name VARCHAR(255),
                                    Age INT,
                                    Gender VARCHAR(255),
                                    ContactNumber VARCHAR(255),
                                    Email VARCHAR(255),
                                    City VARCHAR(255),
                                    EnrollmentYear INT,
                                    Course_Batch VARCHAR(255),
                                    GraduationYear INT
                                )
                            '''
        self.create_table(create_students_query)

# Load Students data        
        students_df = studentdf
        insert_students_query = '''
                            INSERT INTO Students (StudentID, Name, Age, Gender,ContactNumber,Email,City, EnrollmentYear,Course_Batch,GraduationYear)
                            VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE
                            StudentID = VALUES(StudentID),
                            Name = VALUES(Name),
                            Age = VALUES(Age),
                            Gender= VALUES(Gender),
                            ContactNumber = VALUES(ContactNumber),
                            Email=VALUES(Email),
                            City=VALUES(City),
                            EnrollmentYear = VALUES(EnrollmentYear),
                            Course_Batch=VALUES(Course_Batch),
                            GraduationYear=VALUES(GraduationYear)
                            '''
        students_values = students_df.values.tolist()
        self.insert_data(insert_students_query, students_values)

# Create Programming table and insert data from programming_details.csv

        create_programming_table = '''
                                    CREATE TABLE IF NOT EXISTS Programming 
                                    (
                                                ProgrammingID VARCHAR(255) PRIMARY KEY,
                                                StudentID VARCHAR(255),
                                                Language VARCHAR(255),
                                                ProblemsSolved INT,
                                                AssessmentsCompleted INT,
                                                MiniProjects INT,
                                                Certifications INT,
                                                Projectscore INT,
                                                FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
                                    )
                                   '''
        self.create_table(create_programming_table)
        programming_df=programmingdf

        insert_programming_query = '''
                                        INSERT IGNORE INTO Programming (ProgrammingID,StudentID, Language,ProblemsSolved, AssessmentsCompleted,MiniProjects,Certifications,Projectscore)
                                        VALUES (%s, %s, %s, %s,%s, %s,%s,%s)
                                   '''
        programming_values = programming_df.values.tolist()
       
        self.insert_data(insert_programming_query, programming_values)
       
# Create student soft Skills Table 
        create_soft_skills_table = '''
                                   CREATE TABLE IF NOT EXISTS SoftSkills (
                                   SoftSkillID VARCHAR(255) PRIMARY KEY,
                                   StudentID VARCHAR(255),
                                   Communication INT,
                                   Teamwork INT,
                                   Presentation INT,
                                   Leadership INT,
                                   CriticalThinking INT,
                                   Interpersonalskill  INT,
                                   FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
                                    )
                                    '''
        self.create_table(create_soft_skills_table)
        soft_skills_df=softskilldf

        insert_soft_skills_query = '''
                                    INSERT IGNORE INTO SoftSkills (SoftSkillID,StudentID, Communication, Teamwork, Presentation,Leadership,CriticalThinking,Interpersonalskill)
                                    VALUES (%s, %s, %s, %s,%s, %s, %s, %s)
                                   '''
        self.insert_data(insert_soft_skills_query, soft_skills_df.values.tolist())

# Create student placement table.
        create_placements_query = '''
                                  CREATE TABLE IF NOT EXISTS Placements (
                                        PlacementID VARCHAR(255) PRIMARY KEY,
                                        StudentID VARCHAR(255),
                                        MockInterviewScore INT,
                                        InternshipCompleted INT,
                                        PlacementReadiness VARCHAR(255),
                                        CompanyName VARCHAR(255),
                                        FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
                                    )
                                    '''
        self.create_table(create_placements_query)
        placements_df= placementdf

        insert_placements_query = '''
        INSERT IGNORE INTO Placements (PlacementID,StudentID, MockInterviewScore, InternshipCompleted,PlacementReadiness,CompanyName)
        VALUES (%s, %s, %s, %s,%s,%s)
        '''
        self.insert_data(insert_placements_query, placements_df.values.tolist())
        self.close(self)
        
