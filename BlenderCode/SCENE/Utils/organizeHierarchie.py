import bpy

def organize_hierarchie():
    """Organizes objects into respective collections and updates hierarchy."""

    # Create new collections if they don't exist
    collections = {
        "Lighting": None,
        "Planets": None,
        "Camera": None,
        "External Lights": None,
        "SpaceEnvironnement": None  # Correct the name here
    }

    for collection_name in collections:
        if collection_name not in bpy.data.collections:
            new_collection = bpy.data.collections.new(name=collection_name)
            bpy.context.scene.collection.children.link(new_collection)
            collections[collection_name] = new_collection
        else:
            collections[collection_name] = bpy.data.collections[collection_name]

    # Move all objects of each type to their respective collections
    for obj in bpy.context.scene.objects:
        # Unlink the object from all its current collections to avoid duplicates
        for collection in obj.users_collection:
            collection.objects.unlink(obj)

        # Link objects to the appropriate collections based on type or name
        if obj.type == 'LIGHT':  # Area or Point lights, excluding Sun
            if "Sun" in obj.name:
                collections["External Lights"].objects.link(obj)
            else:
                collections["Lighting"].objects.link(obj)
        elif obj.type == 'MESH' and "Sphere" in obj.name:  # MESH (Sphere) go to Planets collection
            collections["Planets"].objects.link(obj)
        elif obj.type == 'CAMERA':  # Cameras go to the Camera collection
            collections["Camera"].objects.link(obj)
        elif "Deep_Space_Stars" in obj.name:  # Deep_Space_Stars in object name (prefix)
            collections["SpaceEnvironnement"].objects.link(obj)  # Corrected to match the collection name

    # Reorganize collections in the Outliner (ensure visibility and hierarchy)
    scene_collections = list(bpy.context.scene.collection.children)

    # Append collections in the desired order
    scene_collections.append(collections["Lighting"])
    scene_collections.insert(1, collections["Planets"])
    scene_collections.insert(2, collections["Camera"])
    scene_collections.insert(3, collections["External Lights"])
    scene_collections.insert(4, collections["SpaceEnvironnement"])  # Corrected name here

    # Make sure collections are linked back to the scene collection for proper Outliner visibility
    for collection in scene_collections:
        bpy.context.scene.collection.children.unlink(collection)
        bpy.context.scene.collection.children.link(collection)

    # Debug: Print the number of objects in each collection for verification
    for collection_name, collection in collections.items():
        print(f"{collection_name} collection objects: {len(collection.objects)}")


def unlink_from_all_collections(obj):
    """Unlink the object from all collections."""
    for collection in obj.collections:
        collection.objects.unlink(obj)


def main():
    print("Executing hierarchie organisation...")
    organize_hierarchie()

if __name__ == "__main__":
    main()