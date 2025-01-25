import streamlit as st
from rdkit import Chem
from rdkit.Chem import Descriptors

def calculate_properties(smiles):
    try:
        molecule = Chem.MolFromSmiles(smiles)
        if molecule is None:
            return None, "No se pudo interpretar la estructura química a partir del SMILES."

        properties = {
            "Masa Molecular": Descriptors.MolWt(molecule),
            "Número de Átomos": molecule.GetNumAtoms(),
            "Número de Enlaces": molecule.GetNumBonds(),
            "Fórmula Molecular": Chem.rdMolDescriptors.CalcMolFormula(molecule)
        }
        return properties, None

    except Exception as e:
        return None, f"Error al calcular propiedades: {str(e)}"

# Configuración de la página
st.title("Calculadora Química")
st.markdown(
    """Esta aplicación permite calcular propiedades químicas como masa molecular,
    número de átomos y fórmula molecular a partir de cadenas **SMILES** o nombres **IUPAC**."""
)

# Entrada del usuario
default_smiles = "CCO"  # Etanol como ejemplo
user_input = st.text_input("Introduce un SMILES o nombre IUPAC:", default_smiles)

# Convertir nombre IUPAC a SMILES si es necesario
if " " in user_input:  # Si el input tiene espacios, podría ser un nombre IUPAC
    try:
        from rdkit.Chem import AllChem
        smiles = Chem.MolToSmiles(AllChem.MolFromName(user_input))
    except Exception:
        smiles = None
else:
    smiles = user_input

# Cálculo de propiedades si hay una entrada válida
if smiles:
    properties, error = calculate_properties(smiles)
    if error:
        st.error(error)
    else:
        st.write("### Propiedades calculadas:")
        for key, value in properties.items():
            st.write(f"- **{key}:** {value}")

        # Mostrar la estructura química
        st.write("### Estructura química:")
        mol = Chem.MolFromSmiles(smiles)
        st.image(Chem.Draw.MolToImage(mol), caption="Estructura generada")
else:
    st.warning("Introduce un SMILES válido o un nombre IUPAC para continuar.")

# Pie de página
st.markdown("Hecho con ❤️ usando Streamlit y RDKit.")

