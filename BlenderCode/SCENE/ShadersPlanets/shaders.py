def create_glass_shader(nodes, node_links, color_primary):
    mix = nodes.new('ShaderNodeMixShader')
    glass1 = nodes.new('ShaderNodeBsdfGlass')
    glass2 = nodes.new('ShaderNodeBsdfGlass')
    glass1.inputs['Color'].default_value = color_primary + (1,)
    glass2.inputs['Color'].default_value = (color_primary[2], color_primary[0], color_primary[1], 1)
    glass1.inputs['IOR'].default_value = 1.4
    glass2.inputs['IOR'].default_value = 1.2
    mix.inputs[0].default_value = 0.5
    node_links.new(glass1.outputs[0], mix.inputs[1])
    node_links.new(glass2.outputs[0], mix.inputs[2])
    return mix

def create_principled_shader(nodes, node_links, color_primary):
    shader = nodes.new("ShaderNodeBsdfPrincipled")
    shader.inputs['Base Color'].default_value = color_primary + (1,)
    shader.inputs['Metallic'].default_value = 0.8
    shader.inputs['Roughness'].default_value = 0.2
    if 'Subsurface' in shader.inputs:
        shader.inputs['Subsurface'].default_value = 0.1
    if 'Clearcoat' in shader.inputs:
        shader.inputs['Clearcoat'].default_value = 0.5
    if 'Sheen' in shader.inputs:
        shader.inputs['Sheen'].default_value = 0.3
    return shader

def create_emission_shader(nodes, node_links, color_primary):
    mix = nodes.new('ShaderNodeMixShader')
    emission1 = nodes.new('ShaderNodeEmission')
    emission2 = nodes.new('ShaderNodeEmission')
    emission1.inputs['Color'].default_value = color_primary + (1,)
    emission2.inputs['Color'].default_value = (color_primary[0] * 1.5, color_primary[1] * 1.5, color_primary[2] * 1.5, 1)
    emission1.inputs['Strength'].default_value = 3.0
    emission2.inputs['Strength'].default_value = 5.0
    mix.inputs[0].default_value = 0.5
    node_links.new(emission1.outputs[0], mix.inputs[1])
    node_links.new(emission2.outputs[0], mix.inputs[2])
    return mix

def create_nebula_shader(nodes, node_links, color_primary):
    mix = nodes.new('ShaderNodeMixShader')
    volume = nodes.new('ShaderNodeVolumePrincipled')
    emission = nodes.new('ShaderNodeEmission')
    volume.inputs['Color'].default_value = color_primary + (1,)
    volume.inputs['Density'].default_value = 0.3
    emission.inputs['Color'].default_value = color_primary + (1,)
    emission.inputs['Strength'].default_value = 2.0
    mix.inputs[0].default_value = 0.7
    node_links.new(volume.outputs[0], mix.inputs[1])
    node_links.new(emission.outputs[0], mix.inputs[2])
    return mix

def create_crystal_emission_shader(nodes, node_links, color_primary):
    mix = nodes.new('ShaderNodeMixShader')
    glass = nodes.new('ShaderNodeBsdfGlass')
    emission = nodes.new('ShaderNodeEmission')
    glass.inputs['Color'].default_value = color_primary + (1,)
    glass.inputs['IOR'].default_value = 1.6
    emission.inputs['Color'].default_value = color_primary + (1,)
    emission.inputs['Strength'].default_value = 1.5
    mix.inputs[0].default_value = 0.3
    node_links.new(glass.outputs[0], mix.inputs[1])
    node_links.new(emission.outputs[0], mix.inputs[2])
    return mix

def create_holographic_shader(nodes, node_links, color_primary):
    mix = nodes.new('ShaderNodeMixShader')
    fresnel = nodes.new('ShaderNodeFresnel')
    glass = nodes.new('ShaderNodeBsdfGlass')
    glossy = nodes.new('ShaderNodeBsdfGlossy')
    glass.inputs['Color'].default_value = color_primary + (1,)
    glossy.inputs['Color'].default_value = (1 - color_primary[0], 1 - color_primary[1], 1 - color_primary[2], 1)
    fresnel.inputs['IOR'].default_value = 1.8
    node_links.new(fresnel.outputs[0], mix.inputs[0])
    node_links.new(glass.outputs[0], mix.inputs[1])
    node_links.new(glossy.outputs[0], mix.inputs[2])
    return mix

def create_solar_fire_shader(nodes, node_links, color_primary):
    mix = nodes.new('ShaderNodeMixShader')
    emission1 = nodes.new('ShaderNodeEmission')
    emission2 = nodes.new('ShaderNodeEmission')
    emission1.inputs['Color'].default_value = (1.0, 0.3, 0.0, 1)
    emission2.inputs['Color'].default_value = (1.0, 0.8, 0.0, 1)
    emission1.inputs['Strength'].default_value = 8.0
    emission2.inputs['Strength'].default_value = 12.0
    mix.inputs[0].default_value = 0.6
    node_links.new(emission1.outputs[0], mix.inputs[1])
    node_links.new(emission2.outputs[0], mix.inputs[2])
    return mix

def create_inferno_shader(nodes, node_links, color_primary):
    mix = nodes.new('ShaderNodeMixShader')
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    emission = nodes.new('ShaderNodeEmission')
    principled.inputs['Base Color'].default_value = (0.1, 0.02, 0.0, 1)
    principled.inputs['Metallic'].default_value = 0.9
    emission.inputs['Color'].default_value = (1.0, 0.2, 0.0, 1)
    emission.inputs['Strength'].default_value = 5.0
    mix.inputs[0].default_value = 0.3
    node_links.new(principled.outputs[0], mix.inputs[1])
    node_links.new(emission.outputs[0], mix.inputs[2])
    return mix
