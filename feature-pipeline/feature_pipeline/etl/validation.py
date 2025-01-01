from great_expectations_core import ExpectationSuite, ExpectationConfiguration

def build_expectaion_suite() -> ExpectationSuite:
    """
    Builder used to retrieve an instance of the validation expectation suite.
    """

    expectation_suite_energy_consumption = ExpectationSuite(
        expectation_suite_name = "energy_consuption_suite"
    )

    # Columns
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_table_columns_to_match_ordered_list",
            kwargs={
                "column_list": [
                    "datetime_utc",
                    "area",
                    "consumer_type",
                    "energy_comsuption",
                ]
            },
        )
    )
    expectation_suite_energy_consumption.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_table_column_count_to_equal", kwargs={"value": 4}
        )
    )

    # Datetime UTC
    expectation_suite_energy_consumption(
        ExpectationConfiguration(
            expectation_type="expect_columns_values_to_not_be_null",
            kwargs={"column": "datetime_utc"},
        )
    )

    # Area
    expectation_suite_energy_consumption(
        ExpectationConfiguration(
            expectation_type="expect_column_distinct_values_to_be_in_set",
            kwargs={"column": "area", "value_set": (0, 1, 2)},
        )
    )


