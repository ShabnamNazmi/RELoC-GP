# Shabnam Nazmi.
# Graduate research assistant at electrical and computer engineering department,
# North Carolina A&T State University, Greensboro, NC.
# snazmi@aggies.ncat.edu.
#
# ------------------------------------------------------------------------------

SEED_NUMBER = 161

DATA_DIR = "D:\Datasets"
DATA_HEADER = "scene"
REPORT_PATH = "report"
NO_FEATURES = 294
NO_LABELS = 6
GET_MLD_PROP = False

REBOOT_MODEL = 1
MAX_ITERATION = 0
MAX_CLASSIFIER = 5000
PROB_HASH = 0.95
DO_SUBSUMPTION = True
AVG_COUNT = 10

PREDICTION_METHOD = 2  # 1: max prediction - 2: aggregated prediction
THRESHOLD = 'OT'
THETA = 0.5
RANK_CUT = 1

K = 2  # number of label clusters
L_MIN = 2

# ------------------------------------------------------------------------------
INIT_FITNESS = 0.01
FITNESS_RED = 0.1
NU = 1
THETA_SUB = 200
LOSS_SUB = 0.01
BETA = 0.1
TRACK_FREQ = 500
ERROR = 1e-3
DELTA = 0.1
THETA_DEL = 20

# GA parameters
SELECTION = 't'   # 'r': roulette wheel selection - 't': tournament selection
P_XOVER = 0.8
P_MUT = 0.04
THETA_GA = 5
