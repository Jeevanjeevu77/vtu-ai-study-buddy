"""
seed.py — Populate the VTU SQLite database with initial data.
Run once:  python seed.py
"""
import sys
from database import engine, SessionLocal, Base
from models import Subject, Note, Question, AptitudeQuestion

# ── Create all tables ──────────────────────────────────────────────────────────
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# ── Seed data ─────────────────────────────────────────────────────────────────
SEED = [
    # ── 2022 / Sem 3 ────────────────────────────────────────────────────────
    {
        "name": "DSA", "code": "DSA", "scheme": "2022", "semester": "3",
        "notes": [
            (0, "Data Structures covers fundamental concepts like arrays, linked lists, stacks, queues, trees, and graphs. Sorting algorithms (Bubble, Merge, Quick), searching (Binary Search), and graph traversals (BFS, DFS) are key topics."),
            (1, "Unit 1: Arrays and Linked Lists — Static vs Dynamic memory, Singly/Doubly/Circular Linked Lists, operations like insertion, deletion, traversal."),
            (2, "Unit 2: Stack & Queue — LIFO for Stack, FIFO for Queue. Applications: expression evaluation, BFS. Implementation using arrays and linked lists."),
            (3, "Unit 3: Trees — Binary Trees, BST, AVL Trees, Heap, B-Trees. Traversals: Inorder, Preorder, Postorder."),
            (4, "Unit 4: Graphs — Representation (Adjacency Matrix/List), BFS, DFS, Spanning Trees, Dijkstra, Prim, Kruskal."),
            (5, "Unit 5: Sorting & Searching — Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort, Heap Sort. Binary Search."),
        ],
        "questions": [
            ("Explain stack with its operations and applications.", "pyq", 1),
            ("Explain queue with its operations and types.", "pyq", 1),
            ("Write an algorithm for Binary Search and analyze its complexity.", "pyq", 5),
            ("Explain AVL tree with rotations and an example.", "pyq", 3),
            ("Explain BFS and DFS with examples.", "pyq", 4),
            ("What is Deadlock?", "pyq", 1),
            ("Compare Merge Sort and Quick Sort with time complexity.", "pyq", 5),
            ("Binary Search", "important", 5),
            ("DFS and BFS", "important", 4),
            ("AVL Rotations", "important", 3),
            ("Explain AVL tree. Write example.", "expected", 3),
            ("Write an algorithm for Merge Sort.", "expected", 5),
        ]
    },
    {
        "name": "Discrete Maths", "code": "DM", "scheme": "2022", "semester": "3",
        "notes": [
            (0, "Discrete Mathematics covers set theory, relations, functions, graph theory, combinatorics, logic, and proof techniques."),
            (1, "Unit 1: Logic — Propositional logic, predicate logic, truth tables, tautologies, logical equivalences."),
            (2, "Unit 2: Set Theory — Sets, Venn diagrams, operations, power sets, Cartesian products."),
            (3, "Unit 3: Relations & Functions — Types of relations, equivalence, partial order, functions, bijections, composition."),
            (4, "Unit 4: Graph Theory — Basic graph concepts, Euler/Hamilton paths, planar graphs, graph coloring."),
            (5, "Unit 5: Combinatorics — Permutations, combinations, pigeonhole principle, recurrence relations."),
        ],
        "questions": [
            ("Define tautology and contradiction with examples.", "pyq", 1),
            ("Explain types of relations with examples.", "pyq", 3),
            ("State and prove the Pigeonhole Principle.", "pyq", 5),
            ("Explain Euler and Hamiltonian paths.", "pyq", 4),
            ("Pigeonhole Principle", "important", 5),
            ("Euler Path", "important", 4),
            ("Explain equivalence relation with an example.", "expected", 3),
        ]
    },
    {
        "name": "Operating System", "code": "OS", "scheme": "2022", "semester": "3",
        "notes": [
            (0, "Operating Systems manage hardware and software resources. Key topics: process management, memory management, file systems, I/O management, deadlocks, and scheduling."),
            (1, "Unit 1: Introduction — OS structure, types, system calls, OS services."),
            (2, "Unit 2: Process Management — Process states, PCB, threads, CPU scheduling algorithms: FCFS, SJF, Priority, Round Robin."),
            (3, "Unit 3: Memory Management — Paging, segmentation, virtual memory, page replacement algorithms (LRU, FIFO, Optimal)."),
            (4, "Unit 4: Deadlocks — Conditions, prevention, avoidance (Banker's Algorithm), detection and recovery."),
            (5, "Unit 5: File Systems — File structure, directory structure, allocation methods, disk scheduling (FCFS, SSTF, SCAN)."),
        ],
        "questions": [
            ("What is Deadlock? Explain necessary conditions for deadlock.", "pyq", 4),
            ("Explain CPU scheduling algorithms with examples.", "pyq", 2),
            ("Explain Banker's Algorithm for deadlock avoidance.", "pyq", 4),
            ("Explain page replacement algorithms: LRU, FIFO, and Optimal.", "pyq", 3),
            ("Explain disk scheduling algorithms.", "pyq", 5),
            ("Deadlock", "important", 4),
            ("Banker's Algorithm", "important", 4),
            ("Round Robin Scheduling", "important", 2),
            ("Explain paging and segmentation.", "expected", 3),
            ("Compare LRU and FIFO page replacement.", "expected", 3),
        ]
    },
    # ── 2022 / Sem 4 ────────────────────────────────────────────────────────
    {
        "name": "Algorithms", "code": "ADA", "scheme": "2022", "semester": "4",
        "notes": [
            (0, "Design and Analysis of Algorithms covers algorithm design paradigms (Divide & Conquer, Greedy, Dynamic Programming, Backtracking) and complexity analysis."),
            (1, "Unit 1: Introduction — Algorithm analysis, asymptotic notation (O, Ω, Θ), recurrence relations, Master Theorem."),
            (2, "Unit 2: Divide & Conquer — Merge Sort, Quick Sort, Binary Search, Strassen's Matrix Multiplication."),
            (3, "Unit 3: Greedy Method — Activity Selection, Huffman Coding, Prim's, Kruskal's, Dijkstra's."),
            (4, "Unit 4: Dynamic Programming — 0/1 Knapsack, LCS, Matrix Chain Multiplication, Floyd-Warshall."),
            (5, "Unit 5: Backtracking & Branch & Bound — N-Queens, Graph Coloring, Subset Sum, TSP."),
        ],
        "questions": [
            ("Explain Merge Sort with example and time complexity.", "pyq", 2),
            ("Solve 0/1 Knapsack using Dynamic Programming.", "pyq", 4),
            ("Explain N-Queens problem using Backtracking.", "pyq", 5),
            ("Explain Huffman Coding with an example.", "pyq", 3),
            ("Explain Master Theorem with examples.", "pyq", 1),
            ("0/1 Knapsack", "important", 4),
            ("N-Queens", "important", 5),
            ("Huffman Coding", "important", 3),
            ("Solve LCS problem using DP.", "expected", 4),
            ("Explain Dijkstra's algorithm.", "expected", 3),
        ]
    },
    {
        "name": "OS", "code": "OS", "scheme": "2022", "semester": "4",
        "notes": [(0, "Advanced OS topics building on Sem 3: Inter-process communication, semaphores, mutex, monitors, and distributed systems introduction.")],
        "questions": [
            ("Explain semaphore and its types.", "pyq", 2),
            ("What is a critical section? Explain solutions.", "pyq", 2),
            ("Semaphores", "important", 2),
            ("Explain monitors in OS.", "expected", 2),
        ]
    },
    {
        "name": "DBMS", "code": "DBMS", "scheme": "2022", "semester": "4",
        "notes": [
            (0, "Database Management Systems — ER diagrams, relational model, SQL, normalization, transaction management, concurrency control."),
            (1, "Unit 1: Introduction — DBMS vs File System, 3-tier architecture, ER model, ER diagrams."),
            (2, "Unit 2: Relational Model — Relational algebra, tuple calculus, SQL DDL & DML."),
            (3, "Unit 3: Normalization — 1NF, 2NF, 3NF, BCNF, 4NF. Functional dependencies, lossless joins."),
            (4, "Unit 4: Transactions — ACID properties, serializability, concurrency control (2PL, Timestamp)."),
            (5, "Unit 5: Storage & Indexing — B+ tree, hashing, query optimization."),
        ],
        "questions": [
            ("Explain Normalization up to BCNF with examples.", "pyq", 3),
            ("What are ACID properties? Explain each.", "pyq", 4),
            ("Explain 2-Phase Locking (2PL) protocol.", "pyq", 4),
            ("Explain B+ Tree with insertion and deletion.", "pyq", 5),
            ("Write SQL queries for joins, group by, having.", "pyq", 2),
            ("ACID Properties", "important", 4),
            ("Normalization", "important", 3),
            ("B+ Tree", "important", 5),
            ("Explain transaction management.", "expected", 4),
            ("Write a detailed ER diagram for a library system.", "expected", 1),
        ]
    },
    # ── 2022 / Sem 5 ────────────────────────────────────────────────────────
    {
        "name": "CN", "code": "CN", "scheme": "2022", "semester": "5",
        "notes": [
            (0, "Computer Networks — OSI and TCP/IP models, IP addressing, routing, transport layer protocols (TCP/UDP), application layer (HTTP, DNS, FTP), network security basics."),
            (1, "Unit 1: Introduction & Physical Layer — Network types, topologies, OSI model layers and functions, transmission media."),
            (2, "Unit 2: Data Link Layer — Framing, error detection (CRC, Checksum), flow control (Stop & Wait, Sliding Window), MAC protocols (CSMA/CD)."),
            (3, "Unit 3: Network Layer — IP addressing (IPv4, IPv6), subnetting, routing algorithms (Dijkstra, Bellman-Ford), OSPF, BGP."),
            (4, "Unit 4: Transport Layer — TCP vs UDP, 3-way handshake, flow control, congestion control."),
            (5, "Unit 5: Application Layer — HTTP, FTP, SMTP, DNS, DHCP, network security (SSL/TLS, firewalls)."),
        ],
        "questions": [
            ("Explain OSI model with functions of each layer.", "pyq", 1),
            ("Explain TCP 3-way handshake.", "pyq", 4),
            ("Explain CRC for error detection with example.", "pyq", 2),
            ("Explain routing algorithms: Dijkstra and Bellman-Ford.", "pyq", 3),
            ("What is subnetting? Solve subnetting problems.", "pyq", 3),
            ("OSI Model", "important", 1),
            ("TCP 3-way Handshake", "important", 4),
            ("CRC Error Detection", "important", 2),
            ("Explain IPv4 and IPv6 differences.", "expected", 3),
            ("Explain DNS and HTTP with examples.", "expected", 5),
        ]
    },
    {
        "name": "TOC", "code": "TOC", "scheme": "2022", "semester": "5",
        "notes": [
            (0, "Theory of Computation — Automata theory (DFA, NFA, PDA), formal languages, grammars (Regular, Context-Free), Turing Machines, decidability, and complexity classes (P vs NP)."),
            (1, "Unit 1: DFA & NFA — Definition, transition diagrams, minimization, equivalence of DFA and NFA."),
            (2, "Unit 2: Regular Languages — Regular expressions, pumping lemma, closure properties."),
            (3, "Unit 3: CFG & PDA — Context-Free Grammars, parse trees, Pushdown Automata, CYK algorithm."),
            (4, "Unit 4: Turing Machines — Definition, variants, decidability, halting problem, undecidability."),
            (5, "Unit 5: Complexity — P, NP, NP-Complete, NP-Hard, reductions."),
        ],
        "questions": [
            ("Explain DFA and NFA with examples. Convert NFA to DFA.", "pyq", 1),
            ("State and prove the Pumping Lemma for Regular Languages.", "pyq", 2),
            ("Explain Pushdown Automata with example.", "pyq", 3),
            ("What is a Turing Machine? Explain its components.", "pyq", 4),
            ("Explain P vs NP problem.", "pyq", 5),
            ("DFA to NFA Conversion", "important", 1),
            ("Pumping Lemma", "important", 2),
            ("Turing Machine", "important", 4),
            ("Design a DFA for strings ending with '01'.", "expected", 1),
            ("Explain halting problem and undecidability.", "expected", 4),
        ]
    },
]

# ── Seed Aptitude Data ──────────────────────────────────────────────────────────
SEED_APTITUDE = [
    {
        "company": "TCS",
        "category": "Quantitative",
        "question": "If a person sells an article for Rs. 650 and gains 30%, what was the cost price?",
        "options": ["Rs. 450", "Rs. 500", "Rs. 550", "Rs. 600"],
        "answer": "B",
        "explanation": "CP = (SP * 100) / (100 + Gain%) = (650 * 100) / 130 = 500."
    },
    {
        "company": "Infosys",
        "category": "Logical",
        "question": "Look at this series: 2, 1, (1/2), (1/4), ... What number should come next?",
        "options": ["(1/3)", "(1/8)", "(2/8)", "(1/16)"],
        "answer": "B",
        "explanation": "This is a geometric series where each number is divided by 2. (1/4)/2 = 1/8."
    },
    {
        "company": "Wipro",
        "category": "Verbal",
        "question": "Choose the synonym for 'Abundant'.",
        "options": ["Scarcity", "Plenty", "Small", "Empty"],
        "answer": "B",
        "explanation": "Abundant means existing in large quantities; plenty."
    }
]

# ── Insert into DB ──────────────────────────────────────────────────────────────
def seed_all():
    db = SessionLocal()
    count_subjects = 0
    count_notes    = 0
    count_questions= 0
    count_aptitude = 0

    print("Seeding subjects and notes...")
    for item in SEED:
        # Check for duplicate
        existing = db.query(Subject).filter_by(
            code=item["code"], scheme=item["scheme"], semester=item["semester"]
        ).first()

        if existing:
            sub = existing
        else:
            sub = Subject(
                name=item["name"],
                code=item["code"],
                scheme=item["scheme"],
                semester=item["semester"],
            )
            db.add(sub)
            db.flush()
            count_subjects += 1

        for (module, content) in item.get("notes", []):
            note = Note(subject_id=sub.id, module=module, content=content)
            db.add(note)
            count_notes += 1

        for q_data in item.get("questions", []):
            text, q_type, unit = q_data
            q = Question(subject_id=sub.id, text=text, q_type=q_type, unit=unit)
            db.add(q)
            count_questions += 1

    print("Seeding aptitude questions...")
    for item in SEED_APTITUDE:
        q = AptitudeQuestion(
            company=item["company"],
            category=item["category"],
            question=item["question"],
            option_a=item["options"][0],
            option_b=item["options"][1],
            option_c=item["options"][2],
            option_d=item["options"][3],
            answer=item["answer"],
            explanation=item["explanation"]
        )
        db.add(q)
        count_aptitude += 1

    db.commit()
    db.close()

    print("DB seeded successfully!")
    print(f"   - {count_subjects} new subjects")
    print(f"   - {count_notes} notes")
    print(f"   - {count_questions} questions")
    print(f"   - {count_aptitude} aptitude questions")

if __name__ == "__main__":
    seed_all()
