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
        return Grade.calkGradeVer11(number)
    def decodeGradeFinal(maxScore, userScore):
        score = userScore/maxScore
        if score > (22 / 27.0):
            return "Senior"
        elif score > (17 / 27.0):
            return "Middle"
        
        return "Junior"
    def decodeGradeFinalNew(maxScore, userScore):
        score = userScore/maxScore
        if score > 0.9:
            return "Senior"
        elif score > 0.7:
            return "Middle+"
        elif score > 0.5:
            return "Middle"
        elif score > 0.4:
            return "Junior+"
        elif score > 0.2:
            return "Junior"
        
        return "Не справились с тестированием"
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
    def maxGrades():
        max = 0
        for num in range(1,100):
            grade = Grade.calkGradeVer(num)
            if grade is not None:
                max += Grade.calkScaleGrade(grade)
        return max
    def calkScaleGrade(grade):
        try:
            if grade is None:
                return 0
            match int(grade):
                case 0:
                    return 1
                case 1:
                    return 1
                case 2:
                    return 3
                case 3:
                    return 3
                case 4:
                    return 5
            return 0
        except Exception:
            pass
