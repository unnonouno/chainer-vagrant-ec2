# coding: utf-8
# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

ec2_config = YAML.load_file('config.yml')

Vagrant.configure(2) do |config|
  config.vm.box = "dummy"

  config.vm.provider :aws do |aws, override|
    aws.access_key_id = ec2_config["access_key_id"]
    aws.secret_access_key = ec2_config["secret_access_key"]
    aws.keypair_name = ec2_config["keypair_name"]

    aws.block_device_mapping = [{"DeviceName" => "/dev/sda1", "Ebs.VolumeSize" => 16}]

    aws.ami = "ami-5189a661"
    aws.instance_type = "g2.2xlarge"
    aws.security_groups = ec2_config["security_groups"]
    aws.region = "us-west-2"

    override.ssh.username = "ubuntu"
    override.ssh.private_key_path = ec2_config["private_key_path"]
  end

  config.vm.provision :fabric do |fabric|
    fabric.fabfile_path = "./fabfile.py"
    fabric.tasks = ["install_chainer_dev"]
  end
end
