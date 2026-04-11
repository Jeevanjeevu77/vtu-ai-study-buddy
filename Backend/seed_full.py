"""
seed_full.py — Populate ALL VTU schemes/semesters with subjects, notes, and questions.
Run:  python seed_full.py
"""
from database import engine, SessionLocal, Base
from models import Subject, Note, Question

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# ══════════════════════════════════════════════════════════════════════════
# FULL DATA — VTU CSE subjects across 2018, 2021, 2022 schemes, Sem 1-8
# ══════════════════════════════════════════════════════════════════════════

FULL_SEED = [
    # ┌──────────────────────────────────────────────────────────────────────┐
    # │                     2022 SCHEME — CSE                               │
    # └──────────────────────────────────────────────────────────────────────┘

    # ── 2022 / Sem 1 (Physics Cycle) ──────────────────────────────────────
    {
        "name": "Mathematics-I", "code": "M1", "scheme": "2022", "semester": "1",
        "notes": [
            (0, "Engineering Mathematics-I covers differential calculus, integral calculus, ordinary differential equations, and vector calculus for first-year engineering students."),
            (1, "Unit 1: Differential Calculus — Successive differentiation, Leibnitz theorem, polar curves, curvature."),
            (2, "Unit 2: Integral Calculus — Reduction formulae, curve tracing, area and volume by integration."),
            (3, "Unit 3: Ordinary Differential Equations — First and higher-order ODEs, exact equations, linear equations."),
            (4, "Unit 4: Vector Calculus — Gradient, divergence, curl, line integrals, Green's theorem, Stokes' theorem."),
        ],
        "questions": [
            ("Find the nth derivative of sin(ax+b).", "pyq", 1),
            ("State and prove Leibnitz theorem.", "pyq", 1),
            ("Evaluate reduction formula for sin^n(x).", "pyq", 2),
            ("Solve the ODE: dy/dx + Py = Q.", "pyq", 3),
            ("State and verify Green's theorem.", "pyq", 4),
            ("Leibnitz Theorem", "important", 1),
            ("Reduction Formulae", "important", 2),
            ("Green's Theorem", "important", 4),
            ("Find the radius of curvature for a given curve.", "expected", 1),
            ("Solve a second order linear ODE with constant coefficients.", "expected", 3),
        ]
    },
    {
        "name": "Applied Physics", "code": "PHY", "scheme": "2022", "semester": "1",
        "notes": [
            (0, "Applied Physics for engineers covers lasers, optical fibers, quantum mechanics, electrical properties of materials, and shock waves/acoustics."),
            (1, "Unit 1: Lasers — Stimulated emission, He-Ne laser, semiconductor laser, applications."),
            (2, "Unit 2: Optical Fibers — Total internal reflection, types of fibers, attenuation, applications in communication."),
            (3, "Unit 3: Quantum Mechanics — Wave-particle duality, de Broglie hypothesis, Heisenberg uncertainty, Schrödinger equation."),
            (4, "Unit 4: Electrical Properties — Band theory, conductors, semiconductors, insulators, Hall effect."),
        ],
        "questions": [
            ("Explain the working of He-Ne laser with energy level diagram.", "pyq", 1),
            ("Derive the expression for numerical aperture of optical fiber.", "pyq", 2),
            ("State de Broglie hypothesis and derive the expression.", "pyq", 3),
            ("Explain Hall effect and its applications.", "pyq", 4),
            ("He-Ne Laser", "important", 1),
            ("Numerical Aperture", "important", 2),
            ("Schrödinger Equation", "important", 3),
            ("Explain types of optical fibers with diagrams.", "expected", 2),
        ]
    },
    {
        "name": "Principles of Programming using C", "code": "PPC", "scheme": "2022", "semester": "1",
        "notes": [
            (0, "Introduction to programming using C language — data types, operators, control flow, functions, arrays, pointers, structures, and file handling."),
            (1, "Unit 1: Basics — Variables, data types, operators, printf/scanf, type conversion."),
            (2, "Unit 2: Control Flow — if-else, switch, for, while, do-while, break, continue."),
            (3, "Unit 3: Functions & Recursion — Function declaration, call by value/reference, recursion, storage classes."),
            (4, "Unit 4: Arrays, Pointers & Structures — 1D/2D arrays, pointer arithmetic, dynamic memory, structures, unions, file I/O."),
        ],
        "questions": [
            ("Write a C program to find factorial using recursion.", "pyq", 3),
            ("Explain pointers and pointer arithmetic with examples.", "pyq", 4),
            ("Differentiate between call by value and call by reference.", "pyq", 3),
            ("Write a program to implement bubble sort.", "pyq", 4),
            ("Explain different storage classes in C.", "pyq", 3),
            ("Recursion", "important", 3),
            ("Pointers", "important", 4),
            ("Structures and Unions", "important", 4),
            ("Write a C program to swap two numbers using pointers.", "expected", 4),
        ]
    },
    {
        "name": "Engineering Drawing", "code": "ED", "scheme": "2022", "semester": "1",
        "notes": [
            (0, "Engineering Drawing covers orthographic projections, projections of points, lines, planes, and solids, isometric views, and development of surfaces."),
        ],
        "questions": [
            ("Draw the projection of a line inclined to both planes.", "pyq", 1),
            ("Draw isometric view from given orthographic views.", "pyq", 1),
            ("Projections of Solids", "important", 1),
        ]
    },

    # ── 2022 / Sem 2 (Chemistry Cycle) ────────────────────────────────────
    {
        "name": "Mathematics-II", "code": "M2", "scheme": "2022", "semester": "2",
        "notes": [
            (0, "Engineering Mathematics-II covers linear algebra, Laplace transforms, Fourier series, and partial differential equations."),
            (1, "Unit 1: Linear Algebra — Rank of matrix, Gauss elimination, eigenvalues, eigenvectors, diagonalization."),
            (2, "Unit 2: Laplace Transforms — Definition, properties, inverse Laplace, convolution theorem, applications to ODEs."),
            (3, "Unit 3: Fourier Series — Periodic functions, Fourier series expansion, half-range series, harmonic analysis."),
            (4, "Unit 4: PDEs — Formation of PDEs, solutions, wave equation, heat equation, Laplace equation."),
        ],
        "questions": [
            ("Find eigenvalues and eigenvectors of a 3x3 matrix.", "pyq", 1),
            ("Find Laplace transform of t*sin(at).", "pyq", 2),
            ("Find Fourier series expansion of f(x) in (-π, π).", "pyq", 3),
            ("Solve the one-dimensional wave equation.", "pyq", 4),
            ("Eigenvalues and Eigenvectors", "important", 1),
            ("Inverse Laplace Transform", "important", 2),
            ("Half-range Fourier Series", "important", 3),
            ("Solve heat equation with boundary conditions.", "expected", 4),
        ]
    },
    {
        "name": "Applied Chemistry", "code": "CHEM", "scheme": "2022", "semester": "2",
        "notes": [
            (0, "Applied Chemistry for engineers — electrochemistry, corrosion, batteries and fuel cells, polymers, water chemistry, and nanomaterials."),
            (1, "Unit 1: Electrochemistry — Electrodes, Nernst equation, electrochemical cells, batteries (Li-ion, lead-acid)."),
            (2, "Unit 2: Corrosion — Types of corrosion, electrochemical theory, prevention methods (galvanic, cathodic protection)."),
            (3, "Unit 3: Polymers — Classification, polymerization, plastics, elastomers, conducting polymers."),
            (4, "Unit 4: Water Chemistry — Hardness, softening (zeolite, ion exchange), desalination, water quality parameters."),
        ],
        "questions": [
            ("Derive the Nernst equation and explain its significance.", "pyq", 1),
            ("Explain electrochemical theory of corrosion.", "pyq", 2),
            ("Differentiate between addition and condensation polymerization.", "pyq", 3),
            ("Explain zeolite process for water softening.", "pyq", 4),
            ("Nernst Equation", "important", 1),
            ("Corrosion Prevention", "important", 2),
            ("Explain Li-ion battery with diagram.", "expected", 1),
        ]
    },
    {
        "name": "Introduction to Python", "code": "PYTHON", "scheme": "2022", "semester": "2",
        "notes": [
            (0, "Introduction to Python programming — syntax, data types, control flow, functions, OOP, file handling, modules, and exception handling."),
            (1, "Unit 1: Python Basics — Variables, data types, operators, input/output, strings, type casting."),
            (2, "Unit 2: Control Flow & Functions — if/elif/else, loops, list/dict comprehensions, functions, lambda, map, filter."),
            (3, "Unit 3: OOP — Classes, objects, inheritance, polymorphism, encapsulation, abstract classes."),
            (4, "Unit 4: File Handling & Modules — Reading/writing files, CSV, JSON, os module, exception handling, pip & packages."),
        ],
        "questions": [
            ("Explain list comprehension with examples.", "pyq", 2),
            ("Write a Python class with inheritance and method overriding.", "pyq", 3),
            ("Explain exception handling: try, except, finally, raise.", "pyq", 4),
            ("Write a Python program to read and write CSV files.", "pyq", 4),
            ("List Comprehension", "important", 2),
            ("Inheritance in Python", "important", 3),
            ("Exception Handling", "important", 4),
            ("Explain lambda, map, and filter with examples.", "expected", 2),
        ]
    },
    {
        "name": "Professional Communication", "code": "ENG", "scheme": "2022", "semester": "2",
        "notes": [
            (0, "Professional Communication covers technical writing, report writing, presentation skills, group discussions, and professional email etiquette."),
        ],
        "questions": [
            ("What are the key elements of a technical report?", "pyq", 1),
            ("Report Writing", "important", 1),
        ]
    },

    # ── 2022 / Sem 6 ──────────────────────────────────────────────────────
    {
        "name": "Software Engineering", "code": "SE", "scheme": "2022", "semester": "6",
        "notes": [
            (0, "Software Engineering covers SDLC models, requirements engineering, software design, testing, project management, and agile methodologies."),
            (1, "Unit 1: Introduction — Software process models: Waterfall, Spiral, Agile, V-Model, Incremental."),
            (2, "Unit 2: Requirements Engineering — SRS document, functional/non-functional requirements, use case diagrams."),
            (3, "Unit 3: Software Design — Architectural design patterns (MVC, Layered), UML diagrams, coupling and cohesion."),
            (4, "Unit 4: Testing — Unit, integration, system, acceptance testing. Black box (equivalence partitioning, boundary value), white box (path, statement coverage)."),
            (5, "Unit 5: Project Management — Estimation (COCOMO, FP), scheduling, risk management, Agile/Scrum practices."),
        ],
        "questions": [
            ("Compare Waterfall and Agile models.", "pyq", 1),
            ("Explain COCOMO model for effort estimation.", "pyq", 5),
            ("Draw UML class diagram and sequence diagram for an ATM system.", "pyq", 3),
            ("Explain black box testing techniques.", "pyq", 4),
            ("What is SRS? Explain its components.", "pyq", 2),
            ("COCOMO Model", "important", 5),
            ("Black Box Testing", "important", 4),
            ("UML Diagrams", "important", 3),
            ("Explain Scrum framework.", "expected", 5),
            ("Draw use case diagram for library management.", "expected", 2),
        ]
    },
    {
        "name": "Compiler Design", "code": "CD", "scheme": "2022", "semester": "6",
        "notes": [
            (0, "Compiler Design covers lexical analysis, syntax analysis, semantic analysis, intermediate code generation, code optimization, and code generation."),
            (1, "Unit 1: Lexical Analysis — Tokens, patterns, regular expressions, finite automata, LEX tool."),
            (2, "Unit 2: Syntax Analysis — CFG, top-down (LL(1)), bottom-up (LR, SLR, LALR) parsing."),
            (3, "Unit 3: Semantic Analysis & ICG — Syntax-directed translation, type checking, three-address code, quadruples, triples."),
            (4, "Unit 4: Code Optimization — Local and global optimization, loop optimization, dead code elimination, peephole optimization."),
            (5, "Unit 5: Code Generation — Register allocation, instruction selection, runtime environments, symbol tables."),
        ],
        "questions": [
            ("Explain the phases of a compiler with a diagram.", "pyq", 1),
            ("Construct LL(1) parsing table for a given grammar.", "pyq", 2),
            ("Generate three-address code for a given expression.", "pyq", 3),
            ("Explain loop optimization techniques.", "pyq", 4),
            ("LL(1) Parsing", "important", 2),
            ("Three-Address Code", "important", 3),
            ("Peephole Optimization", "important", 4),
            ("Construct SLR parsing table.", "expected", 2),
        ]
    },
    {
        "name": "Machine Learning", "code": "ML", "scheme": "2022", "semester": "6",
        "notes": [
            (0, "Machine Learning covers supervised learning, unsupervised learning, regression, classification, clustering, neural networks, and model evaluation."),
            (1, "Unit 1: Introduction — Types of learning, hypothesis space, bias-variance tradeoff, overfitting/underfitting."),
            (2, "Unit 2: Regression & Classification — Linear regression, logistic regression, decision trees, SVM, KNN."),
            (3, "Unit 3: Ensemble Methods — Random Forest, Bagging, Boosting (AdaBoost, XGBoost)."),
            (4, "Unit 4: Unsupervised Learning — K-Means, Hierarchical clustering, PCA, Dimensionality reduction."),
            (5, "Unit 5: Neural Networks — Perceptron, MLP, backpropagation, CNN basics, evaluation metrics (accuracy, precision, recall, F1)."),
        ],
        "questions": [
            ("Explain linear regression with gradient descent.", "pyq", 2),
            ("Explain SVM with kernel trick.", "pyq", 2),
            ("Explain K-Means clustering algorithm.", "pyq", 4),
            ("Explain backpropagation algorithm in neural networks.", "pyq", 5),
            ("What is overfitting? How to prevent it?", "pyq", 1),
            ("SVM with Kernels", "important", 2),
            ("K-Means Clustering", "important", 4),
            ("Backpropagation", "important", 5),
            ("Compare Random Forest and Decision Trees.", "expected", 3),
            ("Explain bias-variance tradeoff.", "expected", 1),
        ]
    },

    # ── 2022 / Sem 7 ──────────────────────────────────────────────────────
    {
        "name": "Artificial Intelligence", "code": "AI", "scheme": "2022", "semester": "7",
        "notes": [
            (0, "Artificial Intelligence covers search algorithms, knowledge representation, reasoning, planning, machine learning foundations, and NLP/robotics basics."),
            (1, "Unit 1: Introduction — AI history, intelligent agents, environments, PEAS."),
            (2, "Unit 2: Search — BFS, DFS, A*, IDA*, minimax, alpha-beta pruning, heuristics."),
            (3, "Unit 3: Knowledge Representation — Propositional logic, first-order logic, resolution, unification."),
            (4, "Unit 4: Planning — STRIPS, partial-order planning, planning graphs."),
            (5, "Unit 5: Probabilistic Reasoning — Bayes' theorem, Bayesian networks, Hidden Markov Models."),
        ],
        "questions": [
            ("Explain A* search algorithm with an example.", "pyq", 2),
            ("Explain minimax algorithm with alpha-beta pruning.", "pyq", 2),
            ("Explain resolution in first-order logic.", "pyq", 3),
            ("What are intelligent agents? Explain types.", "pyq", 1),
            ("Explain Bayesian Networks with an example.", "pyq", 5),
            ("A* Algorithm", "important", 2),
            ("Alpha-Beta Pruning", "important", 2),
            ("Bayesian Networks", "important", 5),
            ("Explain STRIPS planning representation.", "expected", 4),
        ]
    },
    {
        "name": "Cloud Computing", "code": "CC", "scheme": "2022", "semester": "7",
        "notes": [
            (0, "Cloud Computing covers cloud architectures, service models (IaaS, PaaS, SaaS), virtualization, AWS/Azure basics, containerization, and cloud security."),
            (1, "Unit 1: Introduction — Cloud characteristics, deployment models (public, private, hybrid, community)."),
            (2, "Unit 2: Virtualization — Hypervisors (Type 1 & 2), VM migration, containers vs VMs, Docker."),
            (3, "Unit 3: Cloud Services — IaaS, PaaS, SaaS. AWS EC2, S3, Lambda. GCP and Azure overview."),
            (4, "Unit 4: Cloud Security — Identity management, encryption, compliance, multi-tenancy risks."),
        ],
        "questions": [
            ("Compare IaaS, PaaS, and SaaS with examples.", "pyq", 3),
            ("Explain virtualization and compare Type 1 vs Type 2 hypervisors.", "pyq", 2),
            ("What are the cloud deployment models?", "pyq", 1),
            ("Explain Docker and containerization.", "pyq", 2),
            ("IaaS vs PaaS vs SaaS", "important", 3),
            ("Virtualization", "important", 2),
            ("Docker & Containers", "important", 2),
            ("Explain cloud security challenges.", "expected", 4),
        ]
    },
    {
        "name": "Big Data Analytics", "code": "BDA", "scheme": "2022", "semester": "7",
        "notes": [
            (0, "Big Data Analytics covers Hadoop ecosystem, MapReduce, HDFS, Spark, NoSQL databases, and data analytics pipelines."),
            (1, "Unit 1: Introduction — Big Data characteristics (5 V's), challenges, use cases."),
            (2, "Unit 2: Hadoop — HDFS architecture, MapReduce programming model, YARN."),
            (3, "Unit 3: Spark — RDDs, transformations, actions, Spark SQL, Spark Streaming."),
            (4, "Unit 4: NoSQL — MongoDB, Cassandra, HBase. CAP theorem."),
        ],
        "questions": [
            ("Explain HDFS architecture with diagram.", "pyq", 2),
            ("Write a MapReduce program for word count.", "pyq", 2),
            ("Explain CAP theorem.", "pyq", 4),
            ("Compare Hadoop and Spark.", "pyq", 3),
            ("HDFS Architecture", "important", 2),
            ("MapReduce", "important", 2),
            ("CAP Theorem", "important", 4),
            ("Explain Spark RDDs and transformations.", "expected", 3),
        ]
    },

    # ── 2022 / Sem 8 ──────────────────────────────────────────────────────
    {
        "name": "Internet of Things", "code": "IOT", "scheme": "2022", "semester": "8",
        "notes": [
            (0, "IoT covers IoT architectures, protocols (MQTT, CoAP), sensors, Arduino/Raspberry Pi, smart applications, IoT security, and edge/fog computing."),
            (1, "Unit 1: Introduction — IoT definition, architecture (3/5 layer), applications in smart home, agriculture, healthcare."),
            (2, "Unit 2: Protocols — MQTT, CoAP, HTTP, Zigbee, Bluetooth, LoRa, 6LoWPAN."),
            (3, "Unit 3: Hardware — Arduino, Raspberry Pi, sensors (temperature, humidity, ultrasonic), actuators."),
            (4, "Unit 4: Cloud & Analytics — IoT cloud platforms (AWS IoT, ThingSpeak), data analytics."),
            (5, "Unit 5: Security — IoT security challenges, encryption, authentication, edge computing."),
        ],
        "questions": [
            ("Explain IoT architecture with a diagram.", "pyq", 1),
            ("Compare MQTT and CoAP protocols.", "pyq", 2),
            ("Explain the role of Raspberry Pi in IoT with an example project.", "pyq", 3),
            ("What are IoT security challenges?", "pyq", 5),
            ("MQTT vs CoAP", "important", 2),
            ("IoT Architecture", "important", 1),
            ("Explain edge computing vs fog computing.", "expected", 5),
        ]
    },
    {
        "name": "Blockchain Technology", "code": "BCT", "scheme": "2022", "semester": "8",
        "notes": [
            (0, "Blockchain covers distributed ledger technology, cryptographic hash functions, consensus mechanisms, Ethereum, smart contracts, and real-world applications."),
            (1, "Unit 1: Introduction — Blockchain fundamentals, blocks, chains, merkle trees, P2P networks."),
            (2, "Unit 2: Consensus — PoW, PoS, PBFT, Raft, DPoS."),
            (3, "Unit 3: Ethereum — Smart contracts, Solidity, gas, DApps, ERC-20 tokens."),
            (4, "Unit 4: Applications — Supply chain, healthcare, finance, identity management, NFTs."),
        ],
        "questions": [
            ("Explain blockchain structure with merkle tree.", "pyq", 1),
            ("Compare Proof of Work and Proof of Stake.", "pyq", 2),
            ("Write a simple smart contract in Solidity.", "pyq", 3),
            ("PoW vs PoS", "important", 2),
            ("Smart Contracts", "important", 3),
            ("Explain applications of blockchain in supply chain.", "expected", 4),
        ]
    },
    {
        "name": "Project Work", "code": "PROJ", "scheme": "2022", "semester": "8",
        "notes": [(0, "Final year project — apply all CSE concepts to build a real-world application. Includes problem statement, literature survey, design, implementation, testing, and documentation.")],
        "questions": []
    },

    # ┌──────────────────────────────────────────────────────────────────────┐
    # │                     2021 SCHEME — CSE                               │
    # └──────────────────────────────────────────────────────────────────────┘

    # ── 2021 / Sem 1 ──────────────────────────────────────────────────────
    {
        "name": "Mathematics-I", "code": "M1", "scheme": "2021", "semester": "1",
        "notes": [(0, "Engineering Mathematics-I for 2021 scheme — differential calculus (successive differentiation, curve tracing), integral calculus (beta/gamma functions), ODEs, and linear algebra basics.")],
        "questions": [
            ("State and prove Rolle's theorem.", "pyq", 1),
            ("Find the nth derivative of x^n*log(x).", "pyq", 1),
            ("Rolle's Theorem", "important", 1),
            ("Evaluate Beta and Gamma functions.", "expected", 1),
        ]
    },
    {
        "name": "Applied Physics", "code": "PHY", "scheme": "2021", "semester": "1",
        "notes": [(0, "Applied Physics (2021 scheme) — Lasers, optical fibers, quantum mechanics, electrical conductivity, and semiconductors.")],
        "questions": [
            ("Explain Ruby laser with energy level diagram.", "pyq", 1),
            ("Derive expression for numerical aperture.", "pyq", 1),
            ("Ruby Laser", "important", 1),
        ]
    },
    {
        "name": "Introduction to C Programming", "code": "CPC", "scheme": "2021", "semester": "1",
        "notes": [(0, "C Programming (2021 scheme) — data types, operators, control statements, arrays, functions, pointers, structures, file handling.")],
        "questions": [
            ("Write a C program for string manipulation without library functions.", "pyq", 1),
            ("Explain dynamic memory allocation in C.", "pyq", 1),
            ("Pointers and DMA", "important", 1),
        ]
    },

    # ── 2021 / Sem 2 ──────────────────────────────────────────────────────
    {
        "name": "Mathematics-II", "code": "M2", "scheme": "2021", "semester": "2",
        "notes": [(0, "Engineering Mathematics-II (2021) — Laplace transforms, Fourier series, complex analysis, PDEs, and numerical methods.")],
        "questions": [
            ("Find Laplace transform of e^(-at)*sin(bt).", "pyq", 1),
            ("Expand f(x) as Fourier series.", "pyq", 1),
            ("Laplace Transforms", "important", 1),
        ]
    },
    {
        "name": "Applied Chemistry", "code": "CHEM", "scheme": "2021", "semester": "2",
        "notes": [(0, "Applied Chemistry (2021) — Electrochemistry, battery technology, corrosion, polymers, and water treatment.")],
        "questions": [
            ("Explain lithium-ion battery with diagram.", "pyq", 1),
            ("Li-ion Battery", "important", 1),
        ]
    },
    {
        "name": "Introduction to Python Programming", "code": "PYTHON", "scheme": "2021", "semester": "2",
        "notes": [(0, "Python Programming (2021) — Python basics, data structures (lists, tuples, dicts), functions, OOP, NumPy basics, file handling.")],
        "questions": [
            ("Explain list vs tuple vs dictionary in Python.", "pyq", 1),
            ("Write a Python class with constructor and methods.", "pyq", 1),
            ("Python OOP", "important", 1),
        ]
    },

    # ── 2021 / Sem 3 ──────────────────────────────────────────────────────
    {
        "name": "Mathematics-III", "code": "M3", "scheme": "2021", "semester": "3",
        "notes": [(0, "Transform Calculus, Fourier Series and Numerical Techniques — Laplace & inverse Laplace transforms, Fourier transforms, Z-transforms, numerical differentiation & integration, numerical solutions of ODEs.")],
        "questions": [
            ("Find the Z-transform of a^n and n*a^n.", "pyq", 1),
            ("Apply Simpson's 1/3 rule to evaluate an integral.", "pyq", 1),
            ("Z-Transform", "important", 1),
            ("Numerical Methods (Simpson's Rule)", "important", 1),
        ]
    },
    {
        "name": "Data Structures", "code": "DSA", "scheme": "2021", "semester": "3",
        "notes": [
            (0, "Data Structures (2021) — Arrays, linked lists, stacks, queues, trees, graphs, hashing, sorting & searching algorithms."),
            (1, "Unit 1: Stacks — Push, pop, applications (expression evaluation, balancing parentheses)."),
            (2, "Unit 2: Queues — Circular queue, priority queue, deque, applications (BFS)."),
            (3, "Unit 3: Linked Lists — Singly, doubly, circular, operations."),
            (4, "Unit 4: Trees — Binary tree, BST, AVL tree, B-tree, traversals."),
            (5, "Unit 5: Graphs & Hashing — BFS, DFS, Dijkstra, hashing techniques, collision resolution."),
        ],
        "questions": [
            ("Implement stack using linked list.", "pyq", 1),
            ("Explain AVL tree with LL, RR, LR, RL rotations.", "pyq", 4),
            ("Write BFS and DFS algorithms.", "pyq", 5),
            ("Explain hashing with chaining and open addressing.", "pyq", 5),
            ("AVL Tree Rotations", "important", 4),
            ("BFS and DFS", "important", 5),
            ("Explain Dijkstra's shortest path algorithm.", "expected", 5),
        ]
    },
    {
        "name": "Digital Design & Computer Organization", "code": "DDCO", "scheme": "2021", "semester": "3",
        "notes": [(0, "DDCO — Boolean algebra, logic gates, combinational circuits (MUX, decoder, adder), sequential circuits (flip-flops, counters, registers), instruction formats, addressing modes, CPU design, pipelining.")],
        "questions": [
            ("Design a 4-bit binary adder using full adders.", "pyq", 1),
            ("Explain instruction pipelining with hazards.", "pyq", 1),
            ("Pipelining", "important", 1),
            ("Design a 4:1 multiplexer.", "expected", 1),
        ]
    },
    {
        "name": "Object Oriented Programming with Java", "code": "JAVA", "scheme": "2021", "semester": "3",
        "notes": [(0, "OOP with Java — Classes, objects, inheritance, polymorphism, abstraction, interfaces, packages, exception handling, multithreading, I/O, collections framework.")],
        "questions": [
            ("Explain polymorphism with method overloading and overriding.", "pyq", 1),
            ("Write a Java program demonstrating multithreading.", "pyq", 1),
            ("Multithreading", "important", 1),
            ("Explain abstract classes vs interfaces.", "expected", 1),
        ]
    },

    # ── 2021 / Sem 4 ──────────────────────────────────────────────────────
    {
        "name": "Analysis & Design of Algorithms", "code": "ADA", "scheme": "2021", "semester": "4",
        "notes": [(0, "ADA (2021) — Algorithm analysis, divide & conquer, greedy, dynamic programming, backtracking, branch & bound, NP-completeness.")],
        "questions": [
            ("Solve 0/1 Knapsack using DP.", "pyq", 1),
            ("Explain N-Queens using backtracking.", "pyq", 1),
            ("0/1 Knapsack", "important", 1),
            ("Explain P, NP, NP-Complete.", "expected", 1),
        ]
    },
    {
        "name": "Operating Systems", "code": "OS", "scheme": "2021", "semester": "4",
        "notes": [(0, "OS (2021) — Process management, scheduling, synchronization, deadlocks, memory management (paging, segmentation, virtual memory), file systems, I/O systems.")],
        "questions": [
            ("Explain Banker's Algorithm with an example.", "pyq", 1),
            ("Compare paging and segmentation.", "pyq", 1),
            ("Banker's Algorithm", "important", 1),
            ("Explain Round Robin scheduling.", "expected", 1),
        ]
    },
    {
        "name": "Microcontrollers", "code": "MC", "scheme": "2021", "semester": "4",
        "notes": [(0, "Microcontrollers (2021) — ARM architecture, instruction set, memory-mapped I/O, timers, interrupts, embedded C programming, interfacing (LCD, ADC, serial communication).")],
        "questions": [
            ("Explain ARM processor architecture.", "pyq", 1),
            ("Write a program to interface LCD with ARM.", "pyq", 1),
            ("ARM Architecture", "important", 1),
        ]
    },
    {
        "name": "Database Management Systems", "code": "DBMS", "scheme": "2021", "semester": "4",
        "notes": [(0, "DBMS (2021) — ER model, relational algebra, SQL, normalization, transactions, concurrency control, indexing, NoSQL basics.")],
        "questions": [
            ("Explain normalization with examples (1NF to BCNF).", "pyq", 1),
            ("What are ACID properties?", "pyq", 1),
            ("Normalization", "important", 1),
            ("Write SQL queries with joins and subqueries.", "expected", 1),
        ]
    },

    # ── 2021 / Sem 5 ──────────────────────────────────────────────────────
    {
        "name": "Computer Networks", "code": "CN", "scheme": "2021", "semester": "5",
        "notes": [(0, "CN (2021) — OSI & TCP/IP models, data link protocols, IP addressing & subnetting, routing (RIP, OSPF), TCP/UDP, HTTP/DNS/FTP, network security.")],
        "questions": [
            ("Explain OSI model layers with functions.", "pyq", 1),
            ("Compare TCP and UDP.", "pyq", 1),
            ("OSI Model", "important", 1),
            ("Explain subnetting with example.", "expected", 1),
        ]
    },
    {
        "name": "Theory of Computation", "code": "TOC", "scheme": "2021", "semester": "5",
        "notes": [(0, "TOC (2021) — DFA, NFA, regular expressions, pumping lemma, CFG, PDA, Turing machines, decidability, complexity.")],
        "questions": [
            ("Convert NFA to DFA with an example.", "pyq", 1),
            ("Prove a language is not regular using pumping lemma.", "pyq", 1),
            ("NFA to DFA Conversion", "important", 1),
            ("Explain Turing Machine with an example.", "expected", 1),
        ]
    },
    {
        "name": "Software Engineering", "code": "SE", "scheme": "2021", "semester": "5",
        "notes": [(0, "SE (2021) — SDLC models (Waterfall, Agile, Spiral), requirements engineering, design patterns, testing, project estimation (COCOMO), version control.")],
        "questions": [
            ("Compare Waterfall and Agile.", "pyq", 1),
            ("Explain COCOMO estimation model.", "pyq", 1),
            ("Agile Methodology", "important", 1),
        ]
    },

    # ── 2021 / Sem 6 ──────────────────────────────────────────────────────
    {
        "name": "Compiler Design", "code": "CD", "scheme": "2021", "semester": "6",
        "notes": [(0, "CD (2021) — Lexical analysis, parsing (LL, LR), syntax-directed translation, intermediate code, code optimization, code generation.")],
        "questions": [
            ("Construct LL(1) parsing table.", "pyq", 1),
            ("Generate three-address code.", "pyq", 1),
            ("LL(1) Parsing", "important", 1),
        ]
    },
    {
        "name": "Machine Learning", "code": "ML", "scheme": "2021", "semester": "6",
        "notes": [(0, "ML (2021) — Supervised learning (regression, classification, SVM, decision trees), unsupervised (K-Means, PCA), neural networks, model evaluation, ensemble methods.")],
        "questions": [
            ("Explain SVM with kernel trick.", "pyq", 1),
            ("Explain backpropagation.", "pyq", 1),
            ("SVM", "important", 1),
        ]
    },
    {
        "name": "Computer Graphics", "code": "CG", "scheme": "2021", "semester": "6",
        "notes": [(0, "Computer Graphics (2021) — Graphics pipeline, rasterization, 2D/3D transformations, clipping, projections, shading, hidden surface removal, OpenGL.")],
        "questions": [
            ("Explain Bresenham's line drawing algorithm.", "pyq", 1),
            ("Explain 3D transformations (translation, rotation, scaling).", "pyq", 1),
            ("Bresenham's Algorithm", "important", 1),
        ]
    },

    # ── 2021 / Sem 7 ──────────────────────────────────────────────────────
    {
        "name": "Artificial Intelligence", "code": "AI", "scheme": "2021", "semester": "7",
        "notes": [(0, "AI (2021) — Search algorithms (A*, minimax), knowledge representation, logic, probabilistic reasoning, Bayesian networks, NLP, planning.")],
        "questions": [
            ("Explain A* algorithm with example.", "pyq", 1),
            ("Explain Bayesian inference.", "pyq", 1),
            ("A* Algorithm", "important", 1),
        ]
    },
    {
        "name": "Cloud Computing", "code": "CC", "scheme": "2021", "semester": "7",
        "notes": [(0, "Cloud Computing (2021) — Cloud models (IaaS/PaaS/SaaS), virtualization, Docker, Kubernetes, AWS/Azure, cloud security, serverless computing.")],
        "questions": [
            ("Compare IaaS, PaaS, and SaaS.", "pyq", 1),
            ("Explain containerization vs virtualization.", "pyq", 1),
            ("IaaS vs PaaS vs SaaS", "important", 1),
        ]
    },
    {
        "name": "Cryptography", "code": "CRYPTO", "scheme": "2021", "semester": "7",
        "notes": [(0, "Cryptography (2021) — Symmetric (AES, DES), asymmetric (RSA, ECC), hash functions, digital signatures, PKI, network security protocols (SSL/TLS, IPSec).")],
        "questions": [
            ("Explain RSA algorithm with an example.", "pyq", 1),
            ("Compare symmetric and asymmetric encryption.", "pyq", 1),
            ("RSA Algorithm", "important", 1),
        ]
    },

    # ── 2021 / Sem 8 ──────────────────────────────────────────────────────
    {
        "name": "Internet of Things", "code": "IOT", "scheme": "2021", "semester": "8",
        "notes": [(0, "IoT (2021) — IoT architecture, protocols (MQTT, CoAP), sensors, Arduino, Raspberry Pi, cloud integration, smart applications, security.")],
        "questions": [
            ("Explain IoT architecture layers.", "pyq", 1),
            ("Compare MQTT and CoAP.", "pyq", 1),
            ("IoT Architecture", "important", 1),
        ]
    },
    {
        "name": "Deep Learning", "code": "DL", "scheme": "2021", "semester": "8",
        "notes": [(0, "Deep Learning (2021) — CNNs, RNNs, LSTMs, GANs, autoencoders, transfer learning, TensorFlow/PyTorch, image classification, NLP using transformers.")],
        "questions": [
            ("Explain CNN architecture with pooling and convolution layers.", "pyq", 1),
            ("Explain LSTM and its gates.", "pyq", 1),
            ("CNN Architecture", "important", 1),
        ]
    },
    {
        "name": "Project Work", "code": "PROJ", "scheme": "2021", "semester": "8",
        "notes": [(0, "Final year project — real-world CSE application. Includes literature survey, system design, implementation, testing, and documentation.")],
        "questions": []
    },

    # ┌──────────────────────────────────────────────────────────────────────┐
    # │                     2018 SCHEME — CSE                               │
    # └──────────────────────────────────────────────────────────────────────┘

    # ── 2018 / Sem 1 ──────────────────────────────────────────────────────
    {
        "name": "Engineering Mathematics-I", "code": "M1", "scheme": "2018", "semester": "1",
        "notes": [(0, "Engineering Maths-I (2018) — Differential calculus, integral calculus, ODEs, vector calculus.")],
        "questions": [("State and prove Cauchy's mean value theorem.", "pyq", 1), ("Cauchy's MVT", "important", 1)]
    },
    {
        "name": "Engineering Physics", "code": "PHY", "scheme": "2018", "semester": "1",
        "notes": [(0, "Engineering Physics (2018) — Lasers, optical fibers, quantum mechanics, crystal physics, electromagnetic theory.")],
        "questions": [("Explain semiconductor laser.", "pyq", 1), ("Semiconductor Laser", "important", 1)]
    },
    {
        "name": "Basic Electronics", "code": "BEE", "scheme": "2018", "semester": "1",
        "notes": [(0, "Basic Electronics (2018) — Semiconductor devices, diodes, BJT, FET, Op-Amp, digital electronics basics.")],
        "questions": [("Explain working of BJT as amplifier.", "pyq", 1), ("BJT Amplifier", "important", 1)]
    },
    {
        "name": "Elements of Civil Engg", "code": "ECE", "scheme": "2018", "semester": "1",
        "notes": [(0, "Elements of Civil Engineering (2018) — Surveying, building construction, environmental engineering basics.")],
        "questions": [("Explain chain surveying.", "pyq", 1)]
    },

    # ── 2018 / Sem 2 ──────────────────────────────────────────────────────
    {
        "name": "Engineering Mathematics-II", "code": "M2", "scheme": "2018", "semester": "2",
        "notes": [(0, "Engineering Maths-II (2018) — Linear algebra, Laplace transforms, complex analysis, Fourier series.")],
        "questions": [("Find inverse Laplace transform.", "pyq", 1), ("Inverse Laplace", "important", 1)]
    },
    {
        "name": "Engineering Chemistry", "code": "CHEM", "scheme": "2018", "semester": "2",
        "notes": [(0, "Engineering Chemistry (2018) — Electrochemistry, corrosion, polymers, water treatment, nanomaterials, fuels.")],
        "questions": [("Explain galvanic corrosion.", "pyq", 1), ("Corrosion", "important", 1)]
    },
    {
        "name": "C Programming", "code": "CPROG", "scheme": "2018", "semester": "2",
        "notes": [(0, "C Programming (2018) — C fundamentals, control flow, functions, arrays, pointers, structures, file handling.")],
        "questions": [("Write a program to implement linked list in C.", "pyq", 1), ("Pointers in C", "important", 1)]
    },
    {
        "name": "Workshop Practice", "code": "WP", "scheme": "2018", "semester": "2",
        "notes": [(0, "Workshop Practice (2018) — Carpentry, fitting, welding, sheet metal, foundry, smithy.")],
        "questions": []
    },

    # ── 2018 / Sem 3 ──────────────────────────────────────────────────────
    {
        "name": "Engineering Mathematics-III", "code": "M3", "scheme": "2018", "semester": "3",
        "notes": [(0, "Maths-III (2018) — Fourier transforms, Z-transforms, numerical methods, complex analysis, probability & statistics.")],
        "questions": [("Find Z-transform of a given sequence.", "pyq", 1), ("Explain Fast Fourier Transform.", "pyq", 1), ("Z-Transform", "important", 1)]
    },
    {
        "name": "Data Structures", "code": "DSA", "scheme": "2018", "semester": "3",
        "notes": [(0, "Data Structures (2018) — Stacks, queues, linked lists, trees (binary, BST, AVL), graphs (BFS, DFS), hashing, sorting.")],
        "questions": [
            ("Explain AVL tree with rotations.", "pyq", 1), ("Write BFS and DFS algorithms.", "pyq", 1),
            ("AVL Tree", "important", 1), ("Explain hashing techniques.", "expected", 1),
        ]
    },
    {
        "name": "Digital Design & Computer Organization", "code": "DDCO", "scheme": "2018", "semester": "3",
        "notes": [(0, "DDCO (2018) — Combinational & sequential circuits, CPU organization, instruction formats, microprogramming, pipelining.")],
        "questions": [("Explain instruction pipelining.", "pyq", 1), ("Pipelining", "important", 1)]
    },
    {
        "name": "Discrete Mathematics", "code": "DM", "scheme": "2018", "semester": "3",
        "notes": [(0, "Discrete Maths (2018) — Logic, sets, relations, functions, graph theory, combinatorics, algebraic structures.")],
        "questions": [("Prove pigeonhole principle.", "pyq", 1), ("Pigeonhole Principle", "important", 1)]
    },
    {
        "name": "Object Oriented Programming with C++", "code": "OOP", "scheme": "2018", "semester": "3",
        "notes": [(0, "OOP with C++ (2018) — Classes, objects, inheritance, polymorphism, virtual functions, templates, operator overloading, STL, exception handling.")],
        "questions": [("Explain virtual functions and abstract classes.", "pyq", 1), ("Virtual Functions", "important", 1)]
    },

    # ── 2018 / Sem 4 ──────────────────────────────────────────────────────
    {
        "name": "Mathematics-IV", "code": "M4", "scheme": "2018", "semester": "4",
        "notes": [(0, "Maths-IV (2018) — Complex analysis, conformal mapping, special functions (Bessel, Legendre), sampling theory, joint probability, curve fitting.")],
        "questions": [("Explain conformal mapping.", "pyq", 1), ("Bessel Functions", "important", 1)]
    },
    {
        "name": "Analysis & Design of Algorithms", "code": "ADA", "scheme": "2018", "semester": "4",
        "notes": [(0, "ADA (2018) — Algorithm analysis (Big-O), divide and conquer, greedy, DP, backtracking, branch & bound, string matching, NP-completeness.")],
        "questions": [("Solve matrix chain multiplication using DP.", "pyq", 1), ("Explain Kruskal's algorithm.", "pyq", 1), ("Dynamic Programming", "important", 1)]
    },
    {
        "name": "Operating Systems", "code": "OS", "scheme": "2018", "semester": "4",
        "notes": [(0, "OS (2018) — Process scheduling, synchronization (semaphores, monitors), deadlocks, memory management (paging, VM), file systems.")],
        "questions": [("Explain deadlock prevention and avoidance.", "pyq", 1), ("Deadlock", "important", 1), ("Compare preemptive and non-preemptive scheduling.", "expected", 1)]
    },
    {
        "name": "Microprocessors & Microcontrollers", "code": "MP", "scheme": "2018", "semester": "4",
        "notes": [(0, "Microprocessors (2018) — 8086 architecture, instruction set, addressing modes, interrupts, 8255 PPI, 8051 microcontroller.")],
        "questions": [("Explain 8086 architecture.", "pyq", 1), ("8086 Architecture", "important", 1)]
    },
    {
        "name": "Database Management Systems", "code": "DBMS", "scheme": "2018", "semester": "4",
        "notes": [(0, "DBMS (2018) — ER model, relational model, SQL, normalization (1NF-BCNF), transaction processing, concurrency control, B+ trees.")],
        "questions": [("Explain BCNF with example.", "pyq", 1), ("Normalization", "important", 1)]
    },

    # ── 2018 / Sem 5 ──────────────────────────────────────────────────────
    {
        "name": "Computer Networks", "code": "CN", "scheme": "2018", "semester": "5",
        "notes": [(0, "CN (2018) — OSI/TCP-IP models, data link (HDLC, PPP), network layer (IPv4, routing: RIP, OSPF, BGP), transport (TCP, UDP), application (HTTP, DNS, SMTP, FTP).")],
        "questions": [("Explain OSI model.", "pyq", 1), ("Compare RIP and OSPF.", "pyq", 1), ("OSI Model", "important", 1)]
    },
    {
        "name": "Theory of Computation", "code": "TOC", "scheme": "2018", "semester": "5",
        "notes": [(0, "TOC (2018) — Regular languages, DFA, NFA, CFG, PDA, Turing machines, decidability, complexity classes.")],
        "questions": [("Convert NFA to DFA.", "pyq", 1), ("Explain pumping lemma.", "pyq", 1), ("Pumping Lemma", "important", 1)]
    },
    {
        "name": "Software Engineering", "code": "SE", "scheme": "2018", "semester": "5",
        "notes": [(0, "SE (2018) — Software process (Waterfall, Agile, Spiral), requirements, design (UML), testing (unit, integration, system), quality assurance, project management.")],
        "questions": [("Explain Agile methodology.", "pyq", 1), ("Agile Methodology", "important", 1)]
    },
    {
        "name": "Java Programming", "code": "JAVA", "scheme": "2018", "semester": "5",
        "notes": [(0, "Java (2018) — OOP, inheritance, polymorphism, exception handling, multithreading, collections, JDBC, servlets, JSP.")],
        "questions": [("Explain Java collections framework.", "pyq", 1), ("Collections Framework", "important", 1)]
    },

    # ── 2018 / Sem 6 ──────────────────────────────────────────────────────
    {
        "name": "Compiler Design", "code": "CD", "scheme": "2018", "semester": "6",
        "notes": [(0, "CD (2018) — Lexical analysis, parsing (top-down, bottom-up), syntax-directed translation, intermediate code, code optimization, code generation.")],
        "questions": [("Explain phases of a compiler.", "pyq", 1), ("Compiler Phases", "important", 1)]
    },
    {
        "name": "Computer Graphics", "code": "CG", "scheme": "2018", "semester": "6",
        "notes": [(0, "CG (2018) — Line/circle algorithms, 2D/3D transformations, projections, clipping, visible surface detection, illumination models, OpenGL.")],
        "questions": [("Explain DDA and Bresenham's algorithms.", "pyq", 1), ("Bresenham's Algorithm", "important", 1)]
    },
    {
        "name": "Web Technology", "code": "WT", "scheme": "2018", "semester": "6",
        "notes": [(0, "Web Technology (2018) — HTML5, CSS3, JavaScript, PHP, MySQL, AJAX, XML, web services, Node.js basics.")],
        "questions": [("Explain AJAX with an example.", "pyq", 1), ("AJAX", "important", 1)]
    },
    {
        "name": "Cryptography", "code": "CRYPTO", "scheme": "2018", "semester": "6",
        "notes": [(0, "Cryptography (2018) — Classical ciphers, DES, AES, RSA, Diffie-Hellman, digital signatures, PKI, SSL/TLS.")],
        "questions": [("Explain RSA algorithm.", "pyq", 1), ("RSA Algorithm", "important", 1)]
    },

    # ── 2018 / Sem 7 ──────────────────────────────────────────────────────
    {
        "name": "Machine Learning", "code": "ML", "scheme": "2018", "semester": "7",
        "notes": [(0, "ML (2018) — Supervised (regression, SVM, DT), unsupervised (K-Means, PCA), ensemble methods, neural networks, model evaluation.")],
        "questions": [("Explain decision tree algorithm.", "pyq", 1), ("Decision Trees", "important", 1)]
    },
    {
        "name": "Artificial Intelligence", "code": "AI", "scheme": "2018", "semester": "7",
        "notes": [(0, "AI (2018) — Intelligent agents, search algorithms, knowledge representation, logic, planning, probabilistic reasoning.")],
        "questions": [("Explain BFS, DFS, A* algorithms.", "pyq", 1), ("A* Search", "important", 1)]
    },
    {
        "name": "Big Data Analytics", "code": "BDA", "scheme": "2018", "semester": "7",
        "notes": [(0, "BDA (2018) — Hadoop, MapReduce, HDFS, Hive, Pig, Spark, NoSQL (MongoDB, Cassandra), data analytics.")],
        "questions": [("Explain MapReduce programming model.", "pyq", 1), ("MapReduce", "important", 1)]
    },

    # ── 2018 / Sem 8 ──────────────────────────────────────────────────────
    {
        "name": "Internet of Things", "code": "IOT", "scheme": "2018", "semester": "8",
        "notes": [(0, "IoT (2018) — IoT architecture, embedded systems, sensors, MQTT, CoAP, cloud platforms, IoT security, smart applications.")],
        "questions": [("Explain IoT architecture.", "pyq", 1), ("IoT Architecture", "important", 1)]
    },
    {
        "name": "Cloud Computing", "code": "CC", "scheme": "2018", "semester": "8",
        "notes": [(0, "Cloud Computing (2018) — Virtualization, cloud service models, AWS, MapReduce, resource management, cloud security.")],
        "questions": [("Compare public, private, and hybrid cloud.", "pyq", 1), ("Cloud Models", "important", 1)]
    },
    {
        "name": "Project Work", "code": "PROJ", "scheme": "2018", "semester": "8",
        "notes": [(0, "B.E. final year project.")],
        "questions": []
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# INSERT — skip duplicates
# ══════════════════════════════════════════════════════════════════════════════

added_subjects  = 0
added_notes     = 0
added_questions = 0
skipped         = 0

for item in FULL_SEED:
    existing = db.query(Subject).filter_by(
        code=item["code"], scheme=item["scheme"], semester=item["semester"]
    ).first()

    if existing:
        skipped += 1
        continue

    sub = Subject(
        name=item["name"],
        code=item["code"],
        scheme=item["scheme"],
        semester=item["semester"],
    )
    db.add(sub)
    db.flush()
    added_subjects += 1

    for (module, content) in item.get("notes", []):
        db.add(Note(subject_id=sub.id, module=module, content=content))
        added_notes += 1

    for q_data in item.get("questions", []):
        text, q_type, unit = q_data
        db.add(Question(subject_id=sub.id, text=text, q_type=q_type, unit=unit))
        added_questions += 1

db.commit()
db.close()

print("✅ Full seed completed!")
print(f"   → {added_subjects} new subjects added")
print(f"   → {added_notes} notes added")
print(f"   → {added_questions} questions added")
print(f"   → {skipped} subjects skipped (already existed)")
