import os
import sys
import glob
import numpy as np
from numpy.core.numeric import outer
import torch
import utils
import logging
import argparse
import torch.nn as nn
import genotypes
import torch.utils
import torchvision.datasets as dset
import torch.backends.cudnn as cudnn
import random

from torch.autograd import Variable
from model import NetworkCIFAR as Network

from advertorch.attacks import LinfPGDAttack
from advertorch.attacks import GradientSignAttack
from advertorch.attacks import CarliniWagnerL2Attack
from advertorch.context import ctx_noparamgrad_and_eval

parser = argparse.ArgumentParser("cifar")
parser.add_argument('--data', type=str, default='../data', help='location of the data corpus')
parser.add_argument('--batch_size', type=int, default=96, help='batch size')
parser.add_argument('--report_freq', type=float, default=50, help='report frequency')
parser.add_argument('--gpu', type=int, default=0, help='gpu device id')
parser.add_argument('--init_channels', type=int, default=36, help='num of init channels')
parser.add_argument('--layers', type=int, default=20, help='total number of layers')
parser.add_argument('--model_path', type=str, default='EXP/model.pt', help='path of pretrained model')
parser.add_argument('--auxiliary', action='store_true', default=False, help='use auxiliary tower')
parser.add_argument('--cutout', action='store_true', default=False, help='use cutout')
parser.add_argument('--cutout_length', type=int, default=16, help='cutout length')
parser.add_argument('--drop_path_prob', type=float, default=0.2, help='drop path probability')
parser.add_argument('--seed', type=int, default=0, help='random seed')
parser.add_argument('--arch', type=str, default='DARTS', help='which architecture to use')
parser.add_argument('--test_mode', type=str, choices=['CLEAN', 'ADV'], help='choose test mode')
parser.add_argument('--attack', type=str, choices=['PGD10', 'PGD20', 'PGD100', 'FGSM'], help='choose attack')
args = parser.parse_args()

log_format = '%(asctime)s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
    format=log_format, datefmt='%m/%d %I:%M:%S %p')

CIFAR_CLASSES = 10


def main():
  if not torch.cuda.is_available():
    logging.info('no gpu device available')
    sys.exit(1)

  random.seed(args.seed) # ??????????????????314?????????
  np.random.seed(args.seed)
  torch.cuda.set_device(args.gpu)
  cudnn.benchmark = True
  torch.manual_seed(args.seed)
  cudnn.enabled=True
  torch.cuda.manual_seed(args.seed)
  logging.info('gpu device = %d' % args.gpu)
  logging.info("args = %s", args)

  genotype = eval("genotypes.%s" % args.arch)
  model = Network(args.init_channels, CIFAR_CLASSES, args.layers, args.auxiliary, genotype)
  model = model.cuda()
  utils.load(model, args.model_path)

  logging.info("param size = %fMB", utils.count_parameters_in_MB(model))

  criterion = nn.CrossEntropyLoss()
  criterion = criterion.cuda()

  _, test_transform = utils._data_transforms_cifar10(args)
  test_data = dset.CIFAR10(root=args.data, train=False, download=True, transform=test_transform)

  test_queue = torch.utils.data.DataLoader(
      test_data, batch_size=args.batch_size, shuffle=False, pin_memory=True, num_workers=2)

  model.drop_path_prob = args.drop_path_prob
  test_acc, test_obj = infer(test_queue, model, criterion)
  logging.info('test_acc %f', test_acc)


def infer(test_queue, model, criterion):
  objs = utils.AvgrageMeter()
  top1 = utils.AvgrageMeter()
  top5 = utils.AvgrageMeter()
  model.eval()

  if args.attack == 'PGD10':
    adversary = LinfPGDAttack(
    model, loss_fn=nn.CrossEntropyLoss(), eps=8./255,
    nb_iter=10, eps_iter=2./255, rand_init=False, targeted=False)
  
  elif args.attack == 'PGD20':
    adversary = LinfPGDAttack(
    model, loss_fn=nn.CrossEntropyLoss(), eps=8./255,
    nb_iter=20, eps_iter=2./255, rand_init=False, targeted=False)

  elif args.attack == 'PGD100':
    adversary = LinfPGDAttack(
    model, loss_fn=nn.CrossEntropyLoss(), eps=8./255,
    nb_iter=100, eps_iter=2./255, rand_init=False, targeted=False)

  elif args.attack == 'FGSM':
    adversary = GradientSignAttack(
    model, loss_fn = nn.CrossEntropyLoss(), eps=2./255,
      targeted=False)

  #with torch.no_grad():
  for step, (input, target) in enumerate(test_queue):
    with torch.no_grad():
      input = Variable(input, requires_grad=False).cuda()
      target = Variable(target, requires_grad=False).cuda(non_blocking=True)

    if args.test_mode == 'CLEAN':
      logits, _ = model(input)
      loss = criterion(logits, target)

    elif args.test_mode == 'ADV':
      with ctx_noparamgrad_and_eval(model):
        adv_input = adversary.perturb(input, target)
      #print(adv_targeted.size())
      with torch.no_grad():
        logits, _ = model(adv_input)
        loss = criterion(logits, target)
    
    prec1, prec5 = utils.accuracy(logits, target, topk=(1, 5))
    n = input.size(0)
    objs.update(loss.item(), n)
    top1.update(prec1.item(), n)
    top5.update(prec5.item(), n)

    del input
    del target
    del loss

    if step % args.report_freq == 0:
      logging.info('test %03d %e %f %f', step, objs.avg, top1.avg, top5.avg)

  return top1.avg, objs.avg


if __name__ == '__main__':
  main() 
