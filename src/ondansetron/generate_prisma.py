import graphviz
import os

def create_prisma_flowchart():
    """
    Generates a PRISMA 2020 flow diagram using Graphviz.

    The data is based on the 'Study selection' section of the manuscript.
    """
    dot = graphviz.Digraph(
        'PRISMA',
        comment='PRISMA 2020 flow diagram for Ondansetron review'
    )
    dot.attr('graph', rankdir='TB', splines='ortho')
    dot.attr('node', shape='box', style='rounded', fontname='helvetica', fontsize='10')
    dot.attr('edge', fontname='helvetica', fontsize='8')

    # Identification Phase
    dot.node('identification', 
             '<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">'
             '<TR><TD>Records identified from:</TD></TR>'
             '<TR><TD>- Databases (n = 134)</TD></TR>'
             '<TR><TD>- Other sources (n = 0)</TD></TR>'
             '</TABLE>>', 
             shape='plaintext')

    # Screening Phase
    dot.node('screening', 'Records screened (n = 134)')
    dot.node('screening_excluded', 'Records excluded (n = 113)')
    
    # Retrieval Phase
    dot.node('retrieval', 'Reports sought for retrieval (n = 21)')
    dot.node('retrieval_not', 'Reports not retrieved (n = 0)')

    # Eligibility Phase
    dot.node('eligibility', 'Reports assessed for eligibility (n = 21)')
    dot.node('eligibility_excluded', 'Reports excluded (n = 0)')

    # Included
    dot.node('included', 'Studies included in review (n = 21)')

    # Connections
    dot.edge('identification', 'screening')
    dot.edge('screening', 'screening_excluded', label='Exclusion during screening', arrowhead='none')
    dot.edge('screening', 'retrieval')
    dot.edge('retrieval', 'retrieval_not', label='Reports not retrieved', arrowhead='none')
    dot.edge('retrieval', 'eligibility')
    dot.edge('eligibility', 'eligibility_excluded', label='Exclusion during eligibility assessment', arrowhead='none')
    dot.edge('eligibility', 'included')

    # Create ressources directory if it doesn't exist
    if not os.path.exists('ressources'):
        os.makedirs('ressources')

    # Save the flowchart
    output_path = os.path.join('ressources', 'prisma_flowchart')
    dot.render(output_path, format='png', cleanup=True)
    print(f"PRISMA flowchart saved to {output_path}.png")

if __name__ == '__main__':
    create_prisma_flowchart()
