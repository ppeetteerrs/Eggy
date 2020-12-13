import math

# --------------------------------- Settings --------------------------------- #
IMAGE_DIM = 1000  # M,N
BUFFER_DIAG = 70
DRAW_DIAG = 40
TOTAL_DIAG = 200
assert BUFFER_DIAG + DRAW_DIAG < TOTAL_DIAG, "Diagonals Contraints Violated"

BUFFER_DIM = BUFFER_DIAG / math.sqrt(2)
DRAW_DIM = DRAW_DIAG / math.sqrt(2)
TOTAL_DIM = TOTAL_DIAG / math.sqrt(2)
print("Buffer Side Length: {:.2f}, Draw Side Length: {:.2f}".format(BUFFER_DIM, DRAW_DIM))

DIST_THRES = 5
STEP_DIST = 5
AREA_THRES = 0.05

FREQ = 2
