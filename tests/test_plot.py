
def test_plot_module_should_import_plotly_Graph_at_import_time():
    # Given

    # When
    from ddui import plot

    # Then
    assert plot.Graph
    assert plot.Histogram