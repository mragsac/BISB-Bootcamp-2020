# Module 4: Crash Course on High Performance Computing (HPC)

**Module Instructor**: Michelle Franc Ragsac (mragsac@eng.ucsd.edu)

This module serves as an introduction to using high performance computing (HPC) systems effectively for bioinformatics analyses. Unfortunately, we don't have enough time to give an exhaustive course on this topic in two hours time. This module is intended to give students a good introduction and overview of the tools available on the `Triton Shared Compute Cluster (TSCC)` and how to use them effectively!

### Goals of the Module

1. Be able to log into the `Triton Shared Compute Cluster (TSCC)` system with the `ssh` command
2. Run **interactive** and **non-interactive** compute jobs using a job scheduler system (e.g., the `PBS`/`TORQUE`-based job scheduling system offered on `TSCC`)
3. Transfer files to the cluster for analyses using the `wget` command
3. Create and change environments using the `conda` package manager
4. Install packages using the `conda` package manager
5. Launch Jupyter Notebooks with a Python or R kernel
6. Write and Run basic UNIX, Python, and R scripts on the Command Line

---

## Module 4 Set-Up Requirements

<div class="alert alert-block alert-info">
<b>Note:</b> This module requires a terminal application with the ability to securely connect to a remote machine using the "Secure Shell Protocol" (`ssh`).
</div>

The shell (also known as the "terminal" or "command line interface") is a program that allows us to send commands to the computer to recieve some sort of output. Before we start this module, it is important that you install the necessary UNIX Shell program software for your operating system. While we will provide some configuration help at the beginning of the module, it is **highly recommended** that these tools are configured beforehand.

If you need help configuring your system, please refer to Module 1a: Bench to Terminal.