---
id: grade10_computer_studies_architecture_01
title: Computer Organisation and Architecture
subject: Computer Studies
grade: 10
strand: Foundation of Computer Studies
sub_strand: Computer Organisation and Architecture
lesson_number: 2
---

## Learning Objectives

By the end of this lesson, the learner should be able to:

1. Explain the meaning of computer organisation and computer architecture.
2. Identify the major functional units of a computer.
3. Describe the roles of the input unit, processing unit, memory, storage, and output unit.
4. Explain the main components of the Central Processing Unit (CPU).
5. Describe how the functional units of a computer communicate with one another.
6. Explain the basic structure of the von Neumann computer architecture.
7. Describe the fetch-decode-execute cycle.
8. Explain the difference between Reduced Instruction Set Computer (RISC) and Complex Instruction Set Computer (CISC) architectures.
9. Explain the purpose of interfaces, ports, and control signals.
10. Convert numbers between binary, decimal, octal, and hexadecimal systems.
11. Explain how the major components of a computer work together to process information.

---

## Prior Knowledge

Before starting this lesson, the learner should understand:

- The meaning of a computer.
- The difference between hardware and software.
- The basic idea of input, processing, and output.
- Common computer devices such as keyboards, monitors, printers, and storage devices.
- The idea that computers represent information using digital signals.

---

# 1. Introduction to Computer Organisation and Architecture

A computer is made up of many components that work together to receive data, process it, store information, and produce useful results.

For example, when a learner types:

**25 + 15**

into a calculator application, several operations take place.

The input is entered using an input device. The processor receives instructions and performs the calculation. Temporary information may be held in memory, and the result is displayed through an output device.

This gives us the general idea:

**Input → Processing → Storage → Output**

However, a modern computer does much more than simply move information from input to output. Its components communicate through carefully organised structures.

Two related ideas help us understand these structures:

### Computer Organisation

Computer organisation describes **how the physical components of a computer are arranged and how they work together**.

It is concerned with things such as:

- memory
- processors
- registers
- buses
- input and output devices
- control signals
- interfaces

### Computer Architecture

Computer architecture describes **the design and functional behaviour of a computer system as seen by programmers and users**.

It includes concepts such as:

- instruction sets
- processor organisation
- memory organisation
- data representation
- communication between components

A simple way to remember the difference is:

**Architecture → what the computer is designed to do**

**Organisation → how the components are arranged to make it happen**

---

# 2. Functional Units of a Computer

A computer can be divided into several major functional units.

The main units are:

1. Input unit
2. Processing unit
3. Memory
4. Storage
5. Output unit

These units work together as a system.

A simplified representation is:

**Input → Processing ↔ Memory → Output**

Storage provides longer-term storage of programs and data.

The processor may read instructions and data from memory, process them, and store the results back in memory or send them to an output device.

---

# 3. Input Unit

The input unit allows information and instructions to enter a computer system.

Examples of input devices include:

- keyboard
- mouse
- microphone
- scanner
- camera
- touchscreen
- barcode reader

For example, when a learner types a sentence using a keyboard, the keyboard provides the input to the computer.

The input unit helps convert information from a form that humans can provide into signals that the computer can process.

### Example

Suppose a learner enters:

**45**

using a keyboard.

The computer does not process the physical key presses as human-readable numbers. The input system converts them into digital information that the computer can understand.

---

# 4. Processing Unit

The processing unit is responsible for carrying out instructions and manipulating data.

The main processing component is the:

**Central Processing Unit (CPU)**

The CPU is often described as the main processor of a computer.

It performs operations such as:

- arithmetic calculations
- logical comparisons
- controlling operations
- moving information between components
- executing instructions

The CPU contains several important components.

---

# 5. Central Processing Unit

The CPU consists of several functional components, including:

1. Arithmetic and Logic Unit (ALU)
2. Control Unit (CU)
3. Registers

These components work together when the processor executes instructions.

---

## 5.1 Arithmetic and Logic Unit

The **Arithmetic and Logic Unit (ALU)** performs arithmetic and logical operations.

### Arithmetic operations

Examples include:

- addition
- subtraction
- multiplication
- division

### Logical operations

Examples include:

- comparing two values
- checking whether one value is greater than another
- checking whether two values are equal
- performing logical AND, OR, and NOT operations

For example, if a computer needs to determine whether:

**50 > 30**

the ALU can perform the comparison.

The result can be represented as:

**True**

or

**False**

---

## 5.2 Control Unit

The **Control Unit (CU)** coordinates the activities of the computer.

It does not normally perform arithmetic calculations itself.

Instead, it:

- retrieves instructions
- interprets instructions
- sends control signals
- coordinates other components
- controls the sequence in which operations take place

The Control Unit can therefore be thought of as a coordinator.

For example, if an instruction requires data to be loaded from memory and then processed by the ALU, the Control Unit helps coordinate these operations.

---

## 5.3 Registers

Registers are very small and very fast storage locations inside the CPU.

They temporarily hold information that the processor is currently using.

Examples of information held in registers include:

- instructions
- data
- memory addresses
- intermediate results

Registers are much smaller than main memory but provide very fast access to information needed by the CPU.

### Example

If the CPU is performing:

**25 + 15**

it may temporarily hold the values and intermediate results in registers while the ALU performs the calculation.

---

# 6. Memory

Memory holds data and instructions that the CPU needs while a computer is operating.

The most common form of main memory is **Random Access Memory (RAM)**.

RAM is used to temporarily hold:

- programs currently running
- data currently being processed
- intermediate results

RAM is generally volatile.

This means that information stored in RAM is normally lost when power is switched off.

### Example

When a learner opens a word-processing program, the program is loaded into RAM so that the CPU can access the instructions and data needed to run it.

---

# 7. Storage

Storage provides longer-term storage for programs and data.

Examples include:

- hard disk drives
- solid-state drives
- memory cards
- flash drives

Unlike RAM, storage is generally non-volatile.

This means information can remain stored even when the computer is switched off.

### Example

A learner may save a document called:

**Computer_Studies_Assignment.docx**

The document can remain on the storage device after the computer is switched off.

---

# 8. Output Unit

The output unit allows processed information to be presented to the user.

Examples include:

- monitor
- printer
- speakers
- projector
- headphones

For example, after a computer calculates:

**25 + 15 = 40**

the result may be displayed on a monitor.

The monitor therefore acts as an output device.

---

# 9. How the Functional Units Work Together

The functional units of a computer do not operate independently.

They communicate with one another.

Consider the following example:

A learner opens a calculator and enters:

**20 + 30**

### Step 1: Input

The learner enters the numbers using an input device.

### Step 2: Memory

The information may be placed in memory while the program is running.

### Step 3: Processing

The CPU retrieves the relevant instructions and data.

### Step 4: Calculation

The ALU performs the addition.

**20 + 30 = 50**

### Step 5: Result

The result is stored temporarily and sent to the appropriate output system.

### Step 6: Output

The monitor displays:

**50**

This illustrates how the components cooperate rather than working separately.

---

# 10. System Buses

A computer contains pathways that allow components to communicate.

These pathways are commonly called **buses**.

A bus is a communication pathway used to transfer information between components of a computer system.

Three important types are:

1. Data bus
2. Address bus
3. Control bus

---

## 10.1 Data Bus

The data bus carries actual data between components.

For example, data may travel between:

- CPU and memory
- memory and input/output devices
- CPU and input/output devices

The data bus therefore carries the information being processed.

---

## 10.2 Address Bus

The address bus carries information about **where data should be read from or written to**.

For example, when the CPU needs information stored at a particular memory location, an address identifies that location.

A simple analogy is a postal address.

If you want to send a letter, you need:

**The letter → what is being sent**

**The address → where it should go**

Similarly:

**Data bus → what information is being transferred**

**Address bus → where the information is located or should go**

---

## 10.3 Control Bus

The control bus carries control signals that coordinate activities between components.

Control signals may indicate operations such as:

- read
- write
- interrupt
- timing and coordination

The control bus therefore helps components know what operation should take place.

---

# 11. Von Neumann Architecture

The **von Neumann architecture** is a foundational model for understanding how many computer systems are organised.

The architecture is associated with the idea that:

- programs and data can be stored in memory
- the processor retrieves instructions from memory
- instructions are executed sequentially unless another instruction changes the sequence
- input, processing, memory, and output are connected as parts of one system

The main functional elements are:

1. Input
2. Memory
3. Control unit
4. Arithmetic and Logic Unit
5. Output

The ALU and Control Unit form important parts of the CPU.

A simplified model is:

**Input → Memory ↔ CPU → Output**

The CPU communicates with memory and other components using communication pathways such as buses.

---

# 12. Stored Program Concept

One important idea associated with the von Neumann architecture is the **stored program concept**.

A program consists of instructions that tell the computer what operations to perform.

In a stored-program computer, instructions and data can be stored in memory.

This allows the computer to:

1. retrieve an instruction
2. interpret the instruction
3. execute it
4. retrieve the next instruction
5. continue the process

This approach makes computers programmable and flexible.

For example, the same computer can run:

- a word processor
- a calculator
- a web browser
- a game

The hardware does not need to be completely redesigned for each application. Different programs provide different instructions.

---

# 13. Fetch-Decode-Execute Cycle

The CPU repeatedly follows a basic sequence when processing instructions.

This is commonly called the:

**Fetch-Decode-Execute Cycle**

The three major stages are:

1. Fetch
2. Decode
3. Execute

---

## 13.1 Fetch

During the fetch stage, the CPU retrieves the next instruction from memory.

The address of the instruction is determined using processor registers and control mechanisms.

The instruction is brought into the CPU for processing.

---

## 13.2 Decode

During the decode stage, the Control Unit interprets the instruction.

The CPU determines:

- what operation is required
- what data is involved
- which components need to participate

---

## 13.3 Execute

During the execute stage, the CPU carries out the required operation.

For example, it may:

- perform a calculation
- compare values
- move data
- store information
- communicate with an input/output device

After execution, the CPU proceeds to the next instruction.

The cycle then repeats.

### Simple representation

**Fetch → Decode → Execute → Fetch → Decode → Execute → ...**

---

# 14. Instruction Sets

An **instruction set** is the collection of instructions that a processor is designed to understand and execute.

Instructions can tell the processor to perform operations such as:

- add values
- subtract values
- move data
- compare values
- load information
- store information
- branch to another instruction

Different processor architectures can use different instruction-set designs.

Two commonly discussed approaches are:

- RISC
- CISC

---

# 15. Reduced Instruction Set Computer (RISC)

**RISC** stands for:

**Reduced Instruction Set Computer**

RISC processors are designed around a relatively small and simple set of instructions.

The idea is to make individual instructions relatively simple and efficient.

Characteristics commonly associated with RISC include:

- relatively simple instructions
- emphasis on efficient execution
- many operations performed through combinations of simple instructions
- efficient use of registers

### Example

Instead of using one very complex instruction to perform several operations, a RISC processor may use several simpler instructions.

---

# 16. Complex Instruction Set Computer (CISC)

**CISC** stands for:

**Complex Instruction Set Computer**

CISC processors use a larger and more varied instruction set.

Some instructions can perform several operations.

Characteristics commonly associated with CISC include:

- larger instruction sets
- more complex instructions
- instructions capable of performing multiple operations
- emphasis on providing powerful instructions

---

# 17. RISC and CISC Comparison

| Feature | RISC | CISC |
|---|---|---|
| Meaning | Reduced Instruction Set Computer | Complex Instruction Set Computer |
| Instruction set | Relatively smaller and simpler | Larger and more complex |
| Individual instructions | Generally simpler | May perform several operations |
| Design approach | Simplicity and efficient execution | Rich and powerful instructions |
| Registers | Often makes extensive use of registers | Also uses registers, but design emphasis differs |

It is important not to think of one approach as automatically "better".

Modern processors can use techniques influenced by both design philosophies.

The important idea is that RISC and CISC represent different approaches to designing processor instruction sets.

---

# 18. Computer Interfaces

An **interface** is a point or mechanism through which two systems or components communicate.

In a computer, interfaces allow hardware components and external devices to communicate.

Examples include interfaces for:

- USB devices
- displays
- audio devices
- network connections
- storage devices

An interface can define how information is exchanged between components.

---

# 19. Computer Ports

A **port** is a physical or logical connection used to connect a device to a computer or network.

Common physical ports include:

- USB ports
- HDMI ports
- Ethernet ports
- audio ports

### Example

A learner may connect a flash drive to a USB port.

The port provides the physical connection through which the computer can communicate with the storage device.

Ports may support different communication standards, so a device and port need to be compatible.

---

# 20. Control Signals

Computer components need instructions about when and how to perform operations.

These instructions are communicated using **control signals**.

For example, a control signal may indicate that:

- memory should be read
- data should be written
- a device should respond
- a particular operation should begin

The Control Unit generates or manages many of these signals as it coordinates the processor's activities.

Control signals therefore help maintain the correct sequence of operations.

---

# 21. Number Systems in Computers

Computers represent information using digital signals.

Digital systems commonly use the **binary number system**.

Humans normally use the **decimal number system**.

Other number systems that are useful in computing include:

- binary
- decimal
- octal
- hexadecimal

---

# 22. Decimal Number System

The decimal system uses ten digits:

**0, 1, 2, 3, 4, 5, 6, 7, 8, 9**

It is called **base 10** because it has ten possible digits.

For example:

**345**

means:

**3 × 100 + 4 × 10 + 5 × 1**

Therefore:

**345 = 300 + 40 + 5**

---

# 23. Binary Number System

The binary system uses only two digits:

**0 and 1**

It is called **base 2**.

Each binary digit is called a **bit**.

For example:

**1011**

can be expanded using powers of 2:

| Position | Value |
|---|---:|
| 2³ | 8 |
| 2² | 4 |
| 2¹ | 2 |
| 2⁰ | 1 |

Therefore:

**1011₂**

means:

**1 × 8 + 0 × 4 + 1 × 2 + 1 × 1**

**= 8 + 0 + 2 + 1**

**= 11**

Therefore:

**1011₂ = 11₁₀**

---

# 24. Decimal to Binary Conversion

To convert a decimal number to binary, repeated division by 2 can be used.

### Example: Convert 13 to binary

Divide repeatedly by 2:

**13 ÷ 2 = 6 remainder 1**

**6 ÷ 2 = 3 remainder 0**

**3 ÷ 2 = 1 remainder 1**

**1 ÷ 2 = 0 remainder 1**

Read the remainders from bottom to top:

**1101**

Therefore:

**13₁₀ = 1101₂**

---

# 25. Octal Number System

The octal system uses eight digits:

**0, 1, 2, 3, 4, 5, 6, 7**

It is called **base 8**.

Octal can provide a shorter representation of binary values.

For example:

**101 011₂**

can be grouped into groups of three bits:

**101 | 011**

Convert each group:

**101₂ = 5**

**011₂ = 3**

Therefore:

**101011₂ = 53₈**

---

# 26. Hexadecimal Number System

The hexadecimal system uses sixteen symbols:

**0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F**

It is called **base 16**.

The letters represent values greater than 9:

| Hexadecimal | Decimal |
|---|---:|
| A | 10 |
| B | 11 |
| C | 12 |
| D | 13 |
| E | 14 |
| F | 15 |

Hexadecimal is commonly used because it provides a compact way of representing binary information.

---

# 27. Binary to Hexadecimal Conversion

Binary digits can be grouped into sets of four.

### Example

Convert:

**10101111₂**

Group the digits:

**1010 | 1111**

Now convert each group:

**1010₂ = A₁₆**

**1111₂ = F₁₆**

Therefore:

**10101111₂ = AF₁₆**

---

# 28. Why Computers Use Binary

Electronic computers use components that can represent two distinct states.

These states can be represented as:

**0 → OFF**

**1 → ON**

Although the physical behaviour of modern computer hardware is more complex than a simple light switch, the two-state idea provides a useful introduction to digital representation.

Binary therefore provides a natural way of representing digital information.

Text, numbers, images, sound, and other forms of information can be encoded into digital patterns.

---

# 29. How Computer Components Communicate

The functional units of a computer must communicate continuously.

For example:

1. An input device provides data.
2. The data enters the computer system.
3. Memory holds data and instructions.
4. The CPU retrieves instructions and data.
5. The Control Unit coordinates operations.
6. The ALU performs calculations or logical operations.
7. Results may be stored in memory.
8. Results may be sent to an output device.

Buses and interfaces provide pathways for communication.

This cooperation allows the computer to operate as one system.

---

# 30. Kenyan and Everyday Examples

Computer architecture can be understood using examples from everyday life in Kenya.

### Mobile money systems

When a customer uses a mobile money service, information is entered through a mobile device.

The system processes the request, communicates with servers, updates records, and provides a result.

This involves:

**Input → Processing → Storage → Output**

### Point-of-sale systems

A shop may use a point-of-sale computer to record purchases.

A barcode scanner provides input.

The computer processes the information.

The transaction record may be stored.

A receipt provides output.

### School computer laboratory

In a school computer laboratory:

- keyboards and mice provide input
- CPUs process instructions
- RAM holds active programs
- storage devices keep files
- monitors provide visual output
- network interfaces allow communication between computers

These examples show that computer architecture is not only a theoretical concept. It affects systems used in everyday life.

---

# 31. Common Misconceptions

### Misconception 1: The CPU is the entire computer.

**Correction:** The CPU is an important processing component, but a complete computer system also includes memory, storage, input devices, output devices, communication interfaces, and other components.

### Misconception 2: RAM permanently stores files.

**Correction:** RAM is mainly temporary working memory. Permanent files are normally stored on non-volatile storage devices.

### Misconception 3: The ALU controls the entire computer.

**Correction:** The ALU performs arithmetic and logical operations. The Control Unit coordinates processor operations.

### Misconception 4: Binary is only used for numbers.

**Correction:** Binary representation can be used to represent many types of digital information, including text, images, sound, and instructions.

### Misconception 5: RISC means a processor is weak.

**Correction:** RISC refers to an instruction-set design approach. A RISC processor can be powerful and efficient.

### Misconception 6: A port and a bus are the same thing.

**Correction:** A port is a connection point or interface, while a bus is a communication pathway used to transfer information between components.

---

# 32. Summary

Computer organisation describes how the physical components of a computer are arranged and work together.

Computer architecture describes the design and functional behaviour of a computer system.

The major functional units include:

- input
- processing
- memory
- storage
- output

The CPU contains important components such as:

- Arithmetic and Logic Unit
- Control Unit
- registers

The ALU performs arithmetic and logical operations.

The Control Unit coordinates operations.

Registers provide very fast temporary storage inside the CPU.

Memory holds information needed during processing, while storage provides longer-term storage.

Buses provide communication pathways between components.

The three commonly discussed buses are:

- data bus
- address bus
- control bus

The von Neumann architecture provides an important model for understanding computer organisation. It includes input, memory, processing, and output, with programs and data stored in memory.

The CPU repeatedly performs the:

**Fetch → Decode → Execute**

cycle.

RISC and CISC represent different approaches to designing processor instruction sets.

Computers use number systems such as:

- binary
- decimal
- octal
- hexadecimal

Binary is particularly important because digital computers represent information using two-state digital signals.

---

# 33. Revision Notes

## Key Terms

**Computer organisation:**  
The arrangement and interaction of the physical components of a computer.

**Computer architecture:**  
The design and functional behaviour of a computer system.

**CPU:**  
The main processing unit responsible for executing instructions.

**ALU:**  
The part of the CPU responsible for arithmetic and logical operations.

**Control Unit:**  
The CPU component that coordinates operations.

**Register:**  
A small, fast storage location inside the CPU.

**RAM:**  
Temporary working memory used while programs are running.

**Storage:**  
Non-volatile media used to keep data and programs for longer periods.

**Bus:**  
A communication pathway used to transfer information between components.

**Data bus:**  
Carries data.

**Address bus:**  
Carries information identifying memory locations.

**Control bus:**  
Carries control signals.

**Interface:**  
A mechanism through which systems or components communicate.

**Port:**  
A physical or logical connection used to connect devices.

**Instruction set:**  
The collection of instructions a processor can understand and execute.

**RISC:**  
Reduced Instruction Set Computer.

**CISC:**  
Complex Instruction Set Computer.

**Binary:**  
A base-2 number system using 0 and 1.

**Octal:**  
A base-8 number system.

**Hexadecimal:**  
A base-16 number system using 0–9 and A–F.

---

# 34. Guided Questions

1. What is meant by computer organisation?
2. What is meant by computer architecture?
3. What is the difference between computer organisation and computer architecture?
4. Name five major functional units of a computer.
5. What is the purpose of the input unit?
6. What is the role of the CPU?
7. What are the functions of the ALU?
8. What is the role of the Control Unit?
9. Why are registers important?
10. What is the difference between RAM and storage?
11. What is a system bus?
12. Name three types of buses.
13. What does the data bus carry?
14. What does the address bus carry?
15. What is the purpose of the control bus?
16. What is the von Neumann architecture?
17. What is the stored program concept?
18. What are the three stages of the fetch-decode-execute cycle?
19. What is an instruction set?
20. What is the difference between RISC and CISC?
21. What is an interface?
22. What is a computer port?
23. Why are control signals important?
24. Why is binary important in computing?
25. Convert 13 from decimal to binary.
26. Convert 1011₂ to decimal.
27. Convert 10101111₂ to hexadecimal.
28. Explain how the CPU, memory, input, and output units work together.

---

# 35. Practice Questions

## Question 1

Define the following terms:

a) Computer organisation  
b) Computer architecture  
c) CPU  
d) Register  
e) System bus

---

## Question 2

List the three major components of the CPU and describe the function of each.

---

## Question 3

Explain the difference between RAM and storage.

---

## Question 4

Describe the roles of:

a) Data bus  
b) Address bus  
c) Control bus

---

## Question 5

Explain the fetch-decode-execute cycle.

---

## Question 6

Compare RISC and CISC architectures.

---

## Question 7

Explain the importance of the von Neumann architecture.

---

## Question 8

Convert the following decimal numbers to binary:

a) 5  
b) 10  
c) 15  
d) 20

---

## Question 9

Convert the following binary numbers to decimal:

a) 101₂  
b) 1100₂  
c) 10001₂  
d) 10110₂

---

## Question 10

Convert the following binary numbers to hexadecimal:

a) 1010₂  
b) 1111₂  
c) 10101111₂  
d) 11001010₂

---

## Question 11

A learner types a document using a keyboard and saves it to a computer.

Describe what happens from the moment the learner enters the information until the document is saved.

---

## Question 12

A school wants to purchase computers for a laboratory.

Explain why understanding computer organisation and architecture can help the school make informed decisions about the computers.

---

# 36. Quiz

### Question 1

Which component performs arithmetic and logical operations?

A. Control Unit  
B. ALU  
C. Monitor  
D. Storage device

---

### Question 2

Which component coordinates the activities of the CPU?

A. ALU  
B. Control Unit  
C. Keyboard  
D. Hard disk

---

### Question 3

Which type of memory is mainly used as temporary working memory?

A. RAM  
B. ROM  
C. Flash disk  
D. Hard disk

---

### Question 4

Which bus carries actual data?

A. Address bus  
B. Control bus  
C. Data bus  
D. Power bus

---

### Question 5

Which bus identifies a memory location?

A. Data bus  
B. Address bus  
C. Control bus  
D. Input bus

---

### Question 6

What is the correct order of the CPU instruction cycle?

A. Execute → Fetch → Decode  
B. Decode → Execute → Fetch  
C. Fetch → Decode → Execute  
D. Fetch → Execute → Decode

---

### Question 7

What does RISC stand for?

A. Rapid Instruction System Computer  
B. Reduced Instruction Set Computer  
C. Random Instruction Storage Computer  
D. Reduced Information Storage Computer

---

### Question 8

What does CISC stand for?

A. Complex Instruction Set Computer  
B. Central Instruction Storage Computer  
C. Computer Instruction System Controller  
D. Complex Information Storage Computer

---

### Question 9

Which number system uses only 0 and 1?

A. Decimal  
B. Octal  
C. Hexadecimal  
D. Binary

---

### Question 10

What is the decimal value of 1011₂?

A. 9  
B. 10  
C. 11  
D. 12

---

# 37. Answer Key

## Practice Questions

### Question 1

**a) Computer organisation:**  
The arrangement and interaction of the physical components of a computer.

**b) Computer architecture:**  
The design and functional behaviour of a computer system.

**c) CPU:**  
The main processing unit that executes instructions.

**d) Register:**  
A small, fast storage location inside the CPU.

**e) System bus:**  
A communication pathway used to transfer information between components.

---

### Question 2

The three major CPU components are:

**ALU:** Performs arithmetic and logical operations.

**Control Unit:** Coordinates and controls processor operations.

**Registers:** Provide very fast temporary storage for data, instructions, addresses, and intermediate results.

---

### Question 3

RAM is temporary working memory used while programs are running. Storage is used to keep programs and data for longer periods.

RAM is generally volatile, while storage is generally non-volatile.

---

### Question 4

**Data bus:** Carries data between components.

**Address bus:** Carries information identifying memory locations.

**Control bus:** Carries signals that coordinate operations.

---

### Question 5

The fetch-decode-execute cycle consists of:

**Fetch:** The CPU retrieves an instruction from memory.

**Decode:** The Control Unit interprets the instruction.

**Execute:** The CPU carries out the instruction.

The cycle then repeats for the next instruction.

---

### Question 6

RISC uses a relatively smaller and simpler instruction set, while CISC uses a larger and more complex instruction set.

RISC emphasises simple and efficient instructions, while CISC provides a wider range of more complex instructions.

---

### Question 7

The von Neumann architecture provides a model for organising a computer around input, memory, processing, and output. It also supports the stored-program concept, where instructions and data can be stored in memory.

---

### Question 8

a) **5 = 101₂**

b) **10 = 1010₂**

c) **15 = 1111₂**

d) **20 = 10100₂**

---

### Question 9

a) **101₂ = 5₁₀**

b) **1100₂ = 12₁₀**

c) **10001₂ = 17₁₀**

d) **10110₂ = 22₁₀**

---

### Question 10

a) **1010₂ = A₁₆**

b) **1111₂ = F₁₆**

c) **10101111₂ = AF₁₆**

d) **11001010₂ = CA₁₆**

---

### Question 11

The keyboard provides input to the computer. The information is converted into digital form and processed by the computer. The CPU executes the relevant instructions while RAM temporarily holds the active program and data. When the learner saves the document, the information is written to a storage device so that it can be accessed later.

---

### Question 12

Understanding computer organisation and architecture helps the school compare important features such as processor capability, memory, storage, interfaces, ports, and communication capabilities. This can help the school select computers that meet the needs of learners and teachers.

---

## Quiz Answers

1. **B — ALU**
2. **B — Control Unit**
3. **A — RAM**
4. **C — Data bus**
5. **B — Address bus**
6. **C — Fetch → Decode → Execute**
7. **B — Reduced Instruction Set Computer**
8. **A — Complex Instruction Set Computer**
9. **D — Binary**
10. **C — 11**

---

# 38. Lesson Activity

## Activity: Build a Simple Computer Architecture Model

Work in groups and create a simple diagram showing:

- Input
- Memory
- CPU
- ALU
- Control Unit
- Registers
- Output
- Storage
- Data bus
- Address bus
- Control bus

Use arrows to show how information moves between the components.

Then explain your diagram to another group.

### Challenge

Explain what would happen if the CPU could process instructions but could not communicate with memory.

---

# 39. Reflection

After completing this lesson, think about the following questions:

1. Which computer component do you understand best?
2. Which component was difficult to understand?
3. Why does a computer need memory?
4. Why does the CPU need registers?
5. Why are buses important?
6. How does the fetch-decode-execute cycle allow a computer to run programs?
7. Where do you encounter computer architecture in everyday life?

Remember:

**A computer is not a collection of isolated components. It is a system whose components communicate and cooperate to process information.**