output "fc_function_id" {
  value = "${alicloud_fcv2_function.default.id}/${alicloud_fcv2_function.default.function_name}"
}

output "fc_function_trigger_id" {
  value = "${alicloud_fc_trigger.default.id}/${alicloud_fc_trigger.default.name}"
}