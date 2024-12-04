#imports at the beginning 
import seaborn as sns
from faicons import icon_svg
from shinyswatch import theme
from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 

#dataframe ad load file here if needed
df = palmerpenguins.load_penguins()

#create title and theme
ui.page_opts(title="Penguins dashboard", fillable=True, theme=theme.lux)

#sidebar formatting and labels
with ui.sidebar(title="Filter controls"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000) #slider mass input with label
    ui.input_checkbox_group( #checkbos to select species
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()
    ui.h6("Links") #links on sidebar to github repos
    ui.a(
        "GitHub Source",
        href="https://github.com/tsngh/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://tsngh.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

#selecting number of penguins 
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds"), style="color:#0b5394;"):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal"), style="color:#89055d;"): #showing bill length
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm" #average to one place
 
    with ui.value_box(showcase=icon_svg("ruler-vertical"), style="color:#256969;"): #showing bill depth
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm" #average to one place


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth scatterplot") #title based on selection above

        @render.plot
        def length_depth():
            return sns.scatterplot(  # axis label with theme and units
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    with ui.card(full_screen=True):
        ui.card_header("Penguin data")

        @render.data_frame
        def summary_statistics(): #datagrid labels/headings
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


#ui.include_css(app_dir / "styles.css")

#reaftive calc for filtered penguins datafram
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
