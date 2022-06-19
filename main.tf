provider "google" {
  project = var.PROJECT
  region  = var.REGION
  zone    = var.ZONE
}

module "gce-worker-container" {
  source = "./gce-with-container"

  image           = "ghcr.io/allenjhuang/mydisbot:latest"
  privileged_mode = true
  activate_tty    = false
  env_variables = {
    DISCORD_TOKEN = var.DISCORD_TOKEN
  }
  instance_name = "mydisbot-worker"
  network_name  = "default"
}
