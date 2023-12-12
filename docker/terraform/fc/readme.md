# Ali cloud resources
1. fc function
2. fc timer trigger
# Terraform command for ali cloud
```
- terraform init
- terraform plan -lock=false
# import existed cloud resource
- terraform import alicloud_fc_function.default nomad-marketing-sms-production:cronjob-function
- terraform import alicloud_fc_trigger.default nomad-marketing-sms-production:cronjob-function:cronjob-timer
# destroy existed resources
- terraform destroy -lock=false -auto-approve
# apply new cloud resources
- terraform apply -lock=false -auto-approve
```
# Refer
- [什么是Terraform](https://help.aliyun.com/document_detail/95820.html?spm=a2c4g.95822.0.0.43cf33e4haiyeV)
- [快速入门](https://help.aliyun.com/document_detail/95822.html?spm=a2c4g.95820.0.0.4c4c153c7IFMkl)
- [触发器管理](https://www.alibabacloud.com/help/zh/fc/manage-triggers?spm=a2c63.p38356.0.0.5b0d635ea3TKrA)
- [Terraform fcv2_function](https://registry.terraform.io/providers/aliyun/alicloud/latest/docs/resources/fcv2_function)