# This use ~/.kube/config
provider "kubernetes" {
  config_context_cluster = "minikube"
}

provider "helm" {
  version        = "~> 0.9"
  install_tiller = true
}