from nbgrader.api import Gradebook, MissingEntry
import pandas as pd

def get_students_df(db_name):
    """
    Construye un DataFrame con la información de los estudiantes que
    está almacenada en la base de datos de nbgrader.
    
    Parameters:
    -----------
    db_name: Gradebook
    Base de datos de nbgrader (gradebook.db).

    Returns:
    --------
    DataFrame con la información de los estudiantes.
    
    """
    students = []
    # Revisamos la información de los estudiantes en la base de datos
    print("\nInformación actual de los estudiantes en la base de datos de nbgrader:\n")
    for student in db_name.students:
        student_info = {}
        student_info["Id"] =  student.id
        student_info["Lastname"] =  student.last_name
        student_info["Firstname"] =  student.first_name
        student_info["Email"] =  student.email
        student_info["LMS_user_id"] =  student.lms_user_id
        students.append(student_info)
    return pd.DataFrame(students)
    
def update_students(db_name, students_df):
    """
    Actualiza la lista de estudiantes utilizando la lista de participantes
    del curso obtenida de Moodle.
    
    Parameters:
    -----------
    db_name: Gradebook
    Base de datos de nbgrader (gradebook.db).

    students_df: DataFrame
    Lista de estudiantes en formato DataFrame obtenida del archivo CSV
    generado en el Moodle del curso en la opción de Participantes.
    
    """
    for i, (n, s, e) in enumerate(zip(students_df['Nombre'], 
                                      students_df['Apellido(s)'], 
                                      students_df['Dirección Email'])):
        # Agregamos o actualizamos el nombre y apellido de los estudiantes
        # a la base de datos (gradebook.db)
        db_name.update_or_create_student(e, first_name=n, last_name=s, email=e)

    # Elimina estudiantes agregados por omisión
    print("\nCleaning student list:")
    default_students = ["bitdiddle", "hacker", "reasoner"]
    for ds in default_students:
        try:
            db_name.remove_student(ds)
        except MissingEntry:
            print(f"\t{ds} Not found")
        else:
            print(f"\t{ds} eliminated")

def update_assignments(db_name, name="ps1"):
    """
    Elimina assignments agregados por omisión.
    
    Parameters:
    -----------
    db_name: Gradebook
    Base de datos de nbgrader (gradebook.db).

    name: string
    Nombre del assignment a eliminar.
    """
    print("\nCleaning assignment list:")    
    try:
        db_name.remove_assignment(name)
    except MissingEntry:
        print(f"\t{name} Not found")
    else:
        print(f"\t{name} eliminated")
    
def show_assignments(db_name):
    """
    Muestra la lista de assignments y los archivos que lo componen.

    Parameters:
    -----------
    db_name: Gradebook
    Base de datos de nbgrader (gradebook.db).    
    """
    # Revisar los assignments y sus notebooks
    print(f"\nLista de assignments ({len(db_name.assignments)}):")
    for i, assignment in enumerate(db_name.assignments):
        print(f"{i:>2d} {assignment.name}")
        for j, file in enumerate(assignment.notebooks):
            file = str(file).split("/")[1]
            print(f"{j:>4d} {file[:-1]}")
        print()

def calculate_grades(db_name, a_id, n_id = -1, verb=0):
    """
    Calcula la calificación de una notebook dentro de un assignment.

    Parameters:
    -----------
    db_name: Gradebook
    Base de datos de nbgrader (gradebook.db).    

    a_id: int
    Identificador del assignment a evaluar dentro de la lista completa 
    de assignments de la base de datos.

    n_id: int
    Identificador del notebook a evaluar dentro de la lista completa 
    de notebook del assignment correspondiente. Valor por omisión -1, significa
    que evaluará todas las notebooks del assignment.

    verb: int
    Cuando es 0 no se muestra información, cuando es mayor que 0 se muestra informción.

    Returns:
    --------
    Diccionario con las calificaciones del notebook de todos los estudiantes
    """
    grades = []
    assignment = db_name.assignments[a_id] # obtiene el assignment

    if n_id >= 0:
        notebook = assignment.notebooks[n_id]  # obtiene el Notebook
        print(f"\nEvaluación de la {notebook}\n")
    else:
        print(f"\nEvaluación de todo el assignment: {assignment}\n")

    for student in db_name.students:
        # Diccionario para almacenar la información
        # de la notebook entregada por el estudiante
        student_grades = {}
        student_grades["Id"] = student.id

        if verb > 0:
            print(f"\n {student.first_name} {student.last_name} ")
        
        try:
            # Busca la entrega del alumno correspondiente
            submission = db_name.find_submission(assignment.name, student.id)
            
        except MissingEntry:
            student_grades['Score'] = 0.0
            student_grades['Grades'] = 0.0

            if verb > 0:
                print(f"Notebook NOT FOUND")
                print(f"\tCalificación {student_grades['Grades']:5.2f}")
        else:
            if n_id >= 0:
                sb_nb = submission.notebooks # Lista de notebooks entregadas por el estudiante
                submitted_notebook = sb_nb[n_id] # Notebook entregada por el estudiante a evaluar 
    
                # Cálculo de la calificación final del notebook
                student_grades['Score'] = submitted_notebook.score
                student_grades['Grades'] = round(10 * student_grades['Score'] / (submitted_notebook.max_score), 2)

                if verb > 0:
                    print("Notebook: ", submitted_notebook) 
                    print(f"\tScore {student_grades['Score']} of {submitted_notebook.max_score}")
                    print(f"\tCalificación {student_grades['Grades']:5.2f}")
                    print()
            else:
                student_grades['Score'] = 0.0
                partial_grades = 0.0
                for submitted_notebook in submission.notebooks:
                    # Cálculo de la calificación final del notebook
                    student_grades['Score'] = submitted_notebook.score
                    partial_grades += 10 * student_grades['Score'] / submitted_notebook.max_score
                    if verb > 0:
                        print("Notebook: ", submitted_notebook) 
                        print(f"\tScore {student_grades['Score']} of {submitted_notebook.max_score}")
                        print(f"\tCalificación {student_grades['Grades']:5.2f}")
                        print()
                        
                student_grades['Grades'] = round(partial_grades / len(submission.notebooks), 2)
                    
        grades.append(student_grades)

    return grades

def print_for_moodle(grades):
    """
    Imprime en pantalla las calificaciones de la notebook evaluada.
    Esto debe copiarse y pegarse en:
       "Calificaciones > Reporte Calificador > Importar" 
    y luego seleccionar "Pegar desde hoja de cálculo" y en la 
    sección de "Datos" pegar el resultado de esta función incluyendo
    el encabezado.

    Parameters:
    -----------
    grades: dict
    Diccionario con los resultados de la evaluación, generados por la
    función calculate_grades().
    """
    print("Dirección Email\tgrades")
    for item in grades:
        print(item['Id'],"\t", item['Grades'])
        
# ---------------------------
if __name__ == "__main__":
    db_name = "test.db"# input("Nombre de la base de datos: ")
    db_name = "sqlite:///" + db_name
    students_info = "hecompa2025_courseid_4_participants.csv"
    
    print(f"\nBase de datos: {db_name}")
    print(f"Archivo de Moodle: {students_info}\n")
    
    # Lee info del archivo CSV con la información de los estudiantes proveniente de Moodle (Participants)
    student_df = pd.read_csv(students_info) 
#    print(student_df)

    with Gradebook(db_name) as gb:   
        # Actualizar la info de los estudiantes desde Moodle hacia nbgrader
        update_students(gb, student_df)
    
        # Mostrar la información de la base de datos de nbgrader después de la actualización
        print(get_students_df(gb))

        # Actualiza la lista de assignments
        update_assignments(gb)
        
        # Mostrar la información de los assignments en la base de datos
        show_assignments(gb)

        assignment = int(input("Assignment a evaluar:"))
        notebook   = int(input("Notebook a evaluar:"))
        
        grades = calculate_grades(gb, assignment, notebook, 1)

        print_for_moodle(grades)

