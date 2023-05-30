#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#


library(shiny)
library(ggplot2)

library(shiny)
library(ggplot2)

# Define the UI
ui <- fluidPage(
  titlePanel("A/B Test Comparison"),
  
  sidebarLayout(
    sidebarPanel(
      # Input for the number of conversions and total visitors for Group A
      numericInput("conversionsA", "Conversions - Group A:", value = 100),
      numericInput("visitorsA", "Total Visitors - Group A:", value = 1000),
      
      # Input for the number of conversions and total visitors for Group B
      numericInput("conversionsB", "Conversions - Group B:", value = 120),
      numericInput("visitorsB", "Total Visitors - Group B:", value = 1000)
    ),
    
    mainPanel(
      plotOutput("comparisonPlot")
    )
  )
)

# Define the server logic
server <- function(input, output) {
  # Calculate the conversion rates for Group A and Group B
  conversion_rate_A <- reactive({
    input$conversionsA / input$visitorsA
  })
  
  conversion_rate_B <- reactive({
    input$conversionsB / input$visitorsB
  })
  
  # Create a line plot to compare the conversions over time
  output$comparisonPlot <- renderPlot({
    time <- 1:10  # Example time points
    
    data <- data.frame(Time = time,
                       Group_A_Conversions = conversion_rate_A() * time,
                       Group_B_Conversions = conversion_rate_B() * time)
    
    data_long <- tidyr::pivot_longer(data, -Time, names_to = "Group", values_to = "Conversions")
    
    ggplot(data_long, aes(x = Time, y = Conversions, color = Group)) +
      geom_line() +
      labs(x = "Time", y = "Conversions", color = "Group") +
      scale_color_manual(values = c("blue", "red")) +
      theme_minimal() + ylim(0,1)
  })
}

# Run the app
shinyApp(ui = ui, server = server)