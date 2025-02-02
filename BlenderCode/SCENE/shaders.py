import bpy

def create_glass_shader(nodes, color_primary):
    """Creates a glass shader simulating icy material"""
    shader = nodes.new('ShaderNodeBsdfGlass')
    if 'Base Color' in shader.inputs:
        shader.inputs['Base Color'].default_value = color_primary + (1,)
    shader.inputs['IOR'].default_value = 1.3  # A slightly higher index of refraction to simulate icy material
    return shader

def create_principled_shader(nodes, color_primary):
    """Creates a principled BSDF shader for ice-like material"""
    shader = nodes.new("ShaderNodeBsdfPrincipled")

    if 'Base Color' in shader.inputs:
        shader.inputs['Base Color'].default_value = color_primary + (1,)

    # Specular reflections for Principled BSDF
    if 'Specular' in shader.inputs:
        shader.inputs['Specular'].default_value = 0.5  # Specular reflections for glossy icy look

    # Roughness to simulate the ice surface
    if 'Roughness' in shader.inputs:
        shader.inputs['Roughness'].default_value = 0.1  # Shiny ice surface, low roughness

    # Index of Refraction (IOR)
    if 'IOR' in shader.inputs:
        shader.inputs['IOR'].default_value = 1.3  # Ice refraction index

    return shader

def create_emission_shader(nodes, color_primary):
    """Creates an emission shader with icy glow"""
    shader = nodes.new("ShaderNodeEmission")
    if 'Color' in shader.inputs:
        shader.inputs['Color'].default_value = color_primary + (1,)  # Color for the emission
    shader.inputs['Strength'].default_value = 2.0  # Make it emit some light (for night scenes, higher strength may be used)
    return shader
