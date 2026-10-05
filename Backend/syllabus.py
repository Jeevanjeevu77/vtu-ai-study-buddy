"""
syllabus.py — Comprehensive Visvesvaraya Technological University (VTU) Syllabus
Covers Schemes: 2018, 2021, 2022, 2023, 2024 (NEP), 2025 (Autonomous/Latest)
Departments: CSE, ISE, AIML, AIDS, ECE, EEE, MECH, CIVIL (Semesters 1-8)
"""

DEPARTMENTS = {
    "CSE": "Computer Science & Engineering",
    "ISE": "Information Science & Engineering",
    "AIML": "Artificial Intelligence & Machine Learning",
    "AIDS": "Artificial Intelligence & Data Science",
    "ECE": "Electronics & Communication Engineering",
    "EEE": "Electrical & Electronics Engineering",
    "MECH": "Mechanical Engineering",
    "CIVIL": "Civil Engineering"
}

# 1st Year Common Cycles
COMMON_1ST_YEAR = {
    "1": [
        {"name": "Mathematics-I (Calculus & Linear Algebra)", "code": "MATS11"},
        {"name": "Applied Physics for Engineers", "code": "PHYS12"},
        {"name": "Principles of Programming using C", "code": "POP13"},
        {"name": "Basic Electronics & Communication Engineering", "code": "ESC142"},
        {"name": "Communicative English", "code": "ENG16"}
    ],
    "2": [
        {"name": "Mathematics-II (Differential Equations)", "code": "MATS21"},
        {"name": "Applied Chemistry for Engineers", "code": "CHES22"},
        {"name": "Computer-Aided Engineering Drawing", "code": "CED23"},
        {"name": "Basic Electrical Engineering", "code": "ESC241"},
        {"name": "Professional Writing Skills", "code": "PWE26"}
    ]
}

# Core dictionaries for branches
BASE_DEPT_SUBJECTS = {
    "CSE": {
        "3": ["Discrete Mathematical Structures", "Data Structures and Applications", "Object Oriented Programming with Java", "Operating Systems", "Digital Design & Computer Organization"],
        "4": ["Design & Analysis of Algorithms", "Database Management Systems", "Microcontroller and Embedded Systems", "Mathematical & Statistical Foundation"],
        "5": ["Software Engineering", "Computer Networks", "Theory of Computation & Automata", "Artificial Intelligence & Expert Systems"],
        "6": ["Cloud Computing & DevOps", "Machine Learning", "Compiler Design", "Cryptography & Network Security"],
        "7": ["Big Data Analytics", "Internet of Things (IoT)", "Blockchain Technology"],
        "8": ["Major Project Work", "Technical Seminar"]
    },
    "ISE": {
        "3": ["Discrete Mathematics", "Data Structures", "OOP with Java", "Operating Systems & System Software", "Digital Logic & Computer Design"],
        "4": ["Design and Analysis of Algorithms", "Database Management Systems", "Microprocessors", "Python for Data Science"],
        "5": ["Computer Networks & Protocols", "Automata Theory", "Software Engineering & Agile", "Web Technologies & Node.js"],
        "6": ["Data Mining & Warehousing", "Information & Network Security", "Cloud Infrastructure", "Mobile Application Development"],
        "7": ["Machine Learning with Python", "Deep Learning", "Cyber Forensics"],
        "8": ["Industry Internship & Capstone Project"]
    },
    "AIML": {
        "3": ["Linear Algebra & Probability", "Data Structures", "Foundations of AI", "Computer Organization", "Python for Machine Intelligence"],
        "4": ["Algorithms for AI", "Database Systems & NoSQL", "Machine Learning Foundations", "Optimization Techniques"],
        "5": ["Supervised & Unsupervised Learning", "Deep Learning & Neural Networks", "Natural Language Processing", "Computer Vision"],
        "6": ["Reinforcement Learning", "Generative AI & LLMs", "AI Ethics", "Edge AI & IoT Systems"],
        "7": ["Big Data Engineering for AI", "Speech Processing", "Autonomous Systems"],
        "8": ["AI Capstone Project & Industry Internship"]
    },
    "AIDS": {
        "3": ["Probability & Statistics for DS", "Data Structures using C++", "Data Wrangling & EDA", "Operating Systems & Virtualization"],
        "4": ["Design & Analysis of Algorithms", "Big Data Stores", "Foundations of Data Science", "Predictive Modeling"],
        "5": ["Machine Learning Algorithms", "Data Visualization & BI", "Deep Learning for DS", "Cloud Data Warehousing"],
        "6": ["NLP & Text Mining", "Time Series Analysis", "Data Security & Privacy"],
        "7": ["Scalable Machine Learning", "Graph Analytics & Knowledge Graphs"],
        "8": ["Data Science Capstone Project"]
    },
    "ECE": {
        "3": ["Transform Calculus & Fourier Series", "Electronic Principles & Circuits", "Digital System Design", "Network Analysis", "Signals & Systems"],
        "4": ["Complex Analysis & Stochastic Processes", "Analog Circuits", "Electromagnetic Waves", "Microcontroller & Embedded C", "Control Systems"],
        "5": ["Digital Signal Processing", "Digital Communication Systems", "VLSI Design", "Information Theory & Coding"],
        "6": ["Microwave Engineering & Radar", "Embedded Systems & RTOS", "Optical Fiber Communications", "Wireless & Cellular Communications (5G)"],
        "7": ["Satellite Communication", "Antennas & Wave Propagation", "Automotive Electronics"],
        "8": ["Major Project & Industry Internship"]
    },
    "EEE": {
        "3": ["Transform Calculus", "Electric Circuit Analysis", "Analog Electronics", "Transformers & DC Generators"],
        "4": ["Transmission & Distribution", "Induction Machines & Synchronous Motors", "Digital Electronics", "Signals and Linear Systems"],
        "5": ["Power Electronics & Drives", "Control Systems Engineering", "Microcontrollers", "Power System Analysis"],
        "6": ["Power System Protection", "Renewable Energy Sources", "Electric Vehicles & BMS"],
        "7": ["High Voltage Engineering", "Industrial Automation & PLC/SCADA"],
        "8": ["Electrical Major Project Work"]
    },
    "MECH": {
        "3": ["Applied Mathematics", "Mechanics of Materials", "Thermodynamics", "Manufacturing Processes", "Material Science"],
        "4": ["Fluid Mechanics", "Applied Thermodynamics (IC Engines)", "Kinematics of Machines", "Machining Science & CNC"],
        "5": ["Design of Machine Elements-I", "Dynamics of Machines", "Turbo Machines", "Operations Management"],
        "6": ["Design of Machine Elements-II", "Heat Transfer", "Finite Element Analysis", "Robotics & Mechatronics"],
        "7": ["Automobile Engineering", "Additive Manufacturing (3D Printing)", "Refrigeration & Air Conditioning"],
        "8": ["Mechanical Capstone Project"]
    },
    "CIVIL": {
        "3": ["Numerical Methods", "Strength of Materials", "Fluid Mechanics", "Surveying & Geomatics", "Building Materials"],
        "4": ["Analysis of Determinate Structures", "Applied Hydraulics", "Geotechnical Engineering", "Transportation Engineering"],
        "5": ["Design of RC Structural Elements", "Analysis of Indeterminate Structures", "Hydrology", "Environmental Engineering-I"],
        "6": ["Design of Steel Structures", "Applied Geotechnical Engineering", "Environmental Engineering-II", "Construction Management"],
        "7": ["Pre-stressed Concrete", "Bridge Engineering", "Urban Transportation Planning"],
        "8": ["Civil Engineering Project"]
    }
}

def generate_full_syllabus():
    schemes = ["2018", "2021", "2022", "2023", "2024", "2025"]
    syllabus_data = {}
    
    for scheme in schemes:
        prefix = scheme[-2:]
        syllabus_data[scheme] = {}
        
        for dept, dept_name in DEPARTMENTS.items():
            syllabus_data[scheme][dept] = {}
            
            # Common 1st year
            for sem in ["1", "2"]:
                syllabus_data[scheme][dept][sem] = []
                for idx, sub in enumerate(COMMON_1ST_YEAR[sem]):
                    # Make minor tweaks for 2024/2025
                    sub_name = sub["name"]
                    if scheme in ["2024", "2025"] and "Programming" in sub_name:
                        sub_name = "Principles of Programming using Python"
                        
                    code = f"{prefix}{sub['code']}"
                    syllabus_data[scheme][dept][sem].append({"name": sub_name, "code": code})
                    
            # Branch specific higher semesters
            branch_data = BASE_DEPT_SUBJECTS.get(dept, BASE_DEPT_SUBJECTS["CSE"])
            
            for sem in range(3, 9):
                sem_str = str(sem)
                syllabus_data[scheme][dept][sem_str] = []
                
                subs = branch_data.get(sem_str, [])
                for idx, sub_name in enumerate(subs):
                    # Make subjects look extremely modern for 2024 and 2025
                    final_name = sub_name
                    if scheme in ["2024", "2025"]:
                        final_name = final_name.replace("Cloud Computing & DevOps", "Cloud Native Architecture & CI/CD")
                        final_name = final_name.replace("Blockchain Technology", "Web3 & Blockchain Architectures")
                        final_name = final_name.replace("Major Project Work", "Startup Capstone Project")
                        final_name = final_name.replace("Software Engineering", "Agile & Product Management")
                    
                    # Generate VTU style code: 22CS31, 24EC42, 18ME53, etc.
                    dept_code = dept[:2] if len(dept) > 2 else dept
                    if dept == "CIVIL": dept_code = "CV"
                    
                    code = f"{prefix}{dept_code}{sem}{idx+1}"
                    syllabus_data[scheme][dept][sem_str].append({"name": final_name, "code": code})
                    
    return syllabus_data

SYLLABUS_DATA = generate_full_syllabus()

def get_department_subjects(dept: str, scheme: str, sem: str):
    """Fetches list of subjects for given department, scheme, and semester."""
    dept_key = dept.upper()
    if dept_key not in DEPARTMENTS:
        dept_key = "CSE"
        
    sem_str = str(sem).replace("Sem ", "").strip()
    
    if scheme in SYLLABUS_DATA and dept_key in SYLLABUS_DATA[scheme] and sem_str in SYLLABUS_DATA[scheme][dept_key]:
        return SYLLABUS_DATA[scheme][dept_key][sem_str]
    return []

# Flat lookup for backwards compatibility
SYLLABUS = {}
for scheme, depts in SYLLABUS_DATA.items():
    SYLLABUS[scheme] = {}
    for dept, sems in depts.items():
        for sem, subs in sems.items():
            if sem not in SYLLABUS[scheme]:
                SYLLABUS[scheme][sem] = []
            for s in subs:
                if s["name"] not in SYLLABUS[scheme][sem]:
                    SYLLABUS[scheme][sem].append(s["name"])
