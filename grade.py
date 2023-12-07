class Grade:
    def calkGradeVer11(number):
        grade = 0
        if number > 5:
            grade = 1
        if number > 10:
            grade = 2
        if number > 15:
            grade = 3
        if number > 25:
            grade = 4
        if number > 30:
            grade = None
        return grade
    def calkGradeVer1(number):
        grade = 0
        if number > 2:
            grade = 1
        if number > 4:
            grade = 2
        if number > 6:
            grade = 3
        if number > 8:
            grade = 4
        if number > 10:
            grade = None
        return grade
    def calkGradeVer(number):
        return Grade.calkGradeVer1(number)
    def decodeGradeSimbole(grade):
        if grade is None:
            return "_"
        match int(grade):
            case 0:
                return "Junior"
            case 1:
                return "Junior+"
            case 2:
                return "Middle"
            case 3:
                return "Middle+"
            case 4:
                return "Senior"
        return "+"
    def decodeGrade(grade):
        if grade is None:
            return "_"
        return str(grade)
    def allGrades():
        for num in range(1,100):
            grade = Grade.calkGradeVer(num)
            if grade is None:
                return num-1
        return 0
    
