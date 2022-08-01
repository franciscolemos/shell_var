from utils import options, var_model_accuracy


def accuracy(param):
    vma = var_model_accuracy(param)
    vma.var_model()

if __name__ == "__main__":
    param = options.parse_opt()
    accuracy(param)