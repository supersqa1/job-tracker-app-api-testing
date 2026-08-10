def pytest_addoption(parser):
    parser.addoption(
        "--tcid",
        action="append",
        default=[],
        help="Run tests that match a test case id marker. Can be used multiple times."
    )

def pytest_collection_modifyitems(config, items):
    selected_tcids = config.getoption("--tcid")

    if not selected_tcids:
        return

    selected_items = []
    deselected_items = []

    for item in items:
        tcid_markers = item.iter_markers(name="tcid")
        item_tcids = [marker.args[0] for marker in tcid_markers]

        if any(tcid in selected_tcids for tcid in item_tcids):
            selected_items.append(item)
        else:
            deselected_items.append(item)

    items[:] = selected_items
    config.hook.pytest_deselected(items=deselected_items)
