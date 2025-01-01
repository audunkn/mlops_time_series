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