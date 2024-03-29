1. Quick start
- build image
- dbt guides
https://docs.getdbt.com/guides/manual-install?step=8
postgres-setup: https://docs.getdbt.com/docs/core/connect-data-platform/postgres-setup

1. DBT(data build tool) introduce - T(ETL)
```
dbt（data build tool）是一个开源的数据转换工具，专门用于数据仓库的建模和转换。与传统的ETL工具不同，dbt专注于数据转换和建模部分，而不涉及数据抽取（Extract）和加载（Load）过程。它与现有的数据仓库（如Snowflake、BigQuery、Redshift等）紧密集成，使用SQL来定义转换和模型，使数据工程师能够更轻松地构建、测试和部署数据模型。

一些dbt的关键特点包括：

版本控制和可重复性：dbt模型可以存储在版本控制系统中（如Git），使得团队可以轻松合作、审查和跟踪模型变化。这也确保了模型的可重复性和可维护性。

基于SQL的转换：dbt使用SQL来定义转换和模型。这种方法使得数据工程师可以使用他们熟悉的语言进行建模，无需学习新的编程语言或工具。

依赖管理：dbt允许定义模型之间的依赖关系，自动构建适当的转换顺序。

测试和文档：它支持数据模型的测试功能，使得能够验证数据模型的正确性。同时，还可以生成数据文档，使得数据模型的结构和用途变得清晰明了。

可扩展性：dbt可以与各种数据仓库和BI工具结合使用，支持各种数据源。

dbt在数据团队中越来越受欢迎，因为它简化了数据转换和建模的流程，提高了团队的工作效率，并提供了良好的可维护性和文档化，有助于构建健壮的数据仓库和数据模型。
```
