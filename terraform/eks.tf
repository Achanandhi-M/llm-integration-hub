provider "aws" {
  region = "us-west-2" # Replace with your desired region
}

# Data source to fetch default VPC

data "aws_vpc" "default" {
  default = true
}

# Data source to fetch default subnets

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Create an IAM Role for EKS Cluster

resource "aws_iam_role" "eks_role" {
  name = "eks-cluster-role"

  assume_role_policy = <<EOP
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      }
    }
  ]
}
EOP
}

resource "aws_iam_role_policy_attachment" "eks_policy_attachment" {
  for_each = toset([
    "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy",
    "arn:aws:iam::aws:policy/AmazonEKSVPCResourceController"
  ])

  policy_arn = each.value
  role       = aws_iam_role.eks_role.name
}

# Create an IAM Role for EKS Node Group

resource "aws_iam_role" "node_group_role" {
  name = "eks-node-group-role"

  assume_role_policy = <<EOP
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      }
    }
  ]
}
EOP
}

resource "aws_iam_role_policy_attachment" "node_group_policy_attachment" {
  for_each = toset([
    "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
    "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  ])

  policy_arn = each.value
  role       = aws_iam_role.node_group_role.name
}

# Create EKS Cluster

resource "aws_eks_cluster" "example" {
  name     = "example-eks-cluster"
  role_arn = aws_iam_role.eks_role.arn

  vpc_config {
    subnet_ids = data.aws_subnets.default.ids
  }
}

# Create EKS Node Group

resource "aws_eks_node_group" "example" {
  cluster_name    = aws_eks_cluster.example.name
  node_group_name = "example-node-group"
  node_role_arn   = aws_iam_role.node_group_role.arn
  subnet_ids      = data.aws_subnets.default.ids

  scaling_config {
    desired_size = 1
    max_size     = 1
    min_size     = 1
  }

  instance_types = ["t3.medium"]
}
