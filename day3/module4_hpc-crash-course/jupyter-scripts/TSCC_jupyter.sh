#!/bin/bash

##################################################################
# !!!!! TORQUE/PBS JOB SCRIPT PARAMETERS BELOW THIS HEADER !!!!! #
##################################################################
# All parameters for the job script being with the text: #PBS    #
##################################################################

### The queue (-q) to which the job is being submitted to:
### *hotel is the queue for people using TSCC as a pay-as-you-go model,
### *condo is the queue for people who own nodes on TSCC who need more resources than the nodes they own,
### *glean is the free queue for people who own nodes on TSCC based on open resources,
### *home  is the queue for people who own nodes on TSCC who wish to use the nodes they've purchased
#PBS -q condo

### The name of the job (-N) is set as "analysis-jupyter"
#PBS -N analysis-jupyter

### The output (-o) and error/log file (-e) are set as "analysis-jupyter" 
### with the job ID that is assigned to this job, along with .log or .err
### Note: $PBS_JOBID is useful to embed in the script somewhere to help with debugging 
#PBS -o analysis-jupyter.$PBS_JOBID.log
#PBS -e analysis-jupyter.$PBS_JOBID.err

### With the two commands below, we are requesting resources for the job with the (-l) flag
### In the first line, we're requesting a single node/computer (nodes=1) with 2 processors per node (ppn=2)
### In the second line, we're requesting a walltime of 1 hour, 0 minutes, 0 seconts for the job (walltime=01:00:00)
#PBS -l nodes=1:ppn=2
#PBS -l walltime=01:00:00

### With the next line we can specify the email(s) to recieve dianogistc information about the job 
### (If you would like to include multiple emails, separate them with commas!)
#PBS -M mragsac@eng.ucsd.edu

### The (-m) flag designates the type of notifications to recieve: 
### n : [N]o mail sent      a : mail sent with job [A]borted 
###                         b : mail sent when job [B]egins
###                         e : mail sent when job [E]nds/terminates
#PBS -m n

##### Exports all user environment variables to the job (-V)
#PBS -V

#######################################################

### More information about job submission scripts can be found in the TSCC User Guide:
### --------------> https://www.sdsc.edu/support/user_guides/tscc.html <--------------

#######################################################
# !!!!! DIAGNOSTIC STATEMENTS BELOW THIS HEADER !!!!! #
#######################################################

# Print out diagnostic information to have within the output file,
# This information can be removed or kept as desired

echo ------------------------------------------------------
echo -n 'Job is running on node '; cat $PBS_NODEFILE
echo ------------------------------------------------------
echo PBS: qsub is running on $PBS_O_HOST
echo PBS: originating queue is $PBS_O_QUEUE
echo PBS: executing queue is $PBS_QUEUE
echo PBS: working directory is $PBS_O_WORKDIR
echo PBS: execution mode is $PBS_ENVIRONMENT
echo PBS: job identifier is $PBS_JOBID
echo PBS: job name is $PBS_JOBNAME
echo PBS: node file is $PBS_NODEFILE
echo PBS: current home directory is $PBS_O_HOME
echo PBS: PATH = $PBS_O_PATH
echo ------------------------------------------------------

##############################################
# !!!!! JOB COMMANDS BELOW THIS HEADER !!!!! #
##############################################

# Prints some diagnostic information for debugging later if necessary
echo ""
echo "Current Date: " date
echo "Current Working Directory: " pwd
echo ""

# Change number to be larger than 1024
JUPYTER_PORT=8448

echo "This job starts a remote Jupyter Notebook instance on TSCC!"
echo "Assigned Jupyter Port: " $JUPYTER_PORT
echo ""

# !!! If this script doesn't work, one of the reasons could be that
#     your desired port is already used. In that case, change the number!

##############################################

# Define environments to use with this notebook here;
# Unfortuantely the conda activate convention does not work here, 
# so we have to use a different syntax to activate the environment
# (e.g. source activate [ENVIRONMENT_NAME])

source activate module4_python

##############################################

# Set up the SSH tunnel betweeing the COMPUTING and LOGIN node
# and then launch the notebook without a browser to travel through the tunnel

ssh -N -f -R $JUPYTER_PORT:localhost:$JUPYTER_PORT $PBS_O_HOST
jupyter lab --port=$JUPYTER_PORT --no-browser

# Uncomment the line below if you would like to use jupyter notebooks instead of the jupyter lab interface
# jupyter notebook --port=$JUPYTER_PORT --no-browser