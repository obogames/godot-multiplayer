extends Node

var prev_scene: String = ""

var _master_scene: PackedScene = null


var current_scene: String:
	get:
		return _get_current(get_tree())


## Unloads current scene & loads target scene
func change_scene(scene_path: String, follow_history = true) -> void:
	if not scene_path:
		return

	call_deferred("_request_scene_change", scene_path, follow_history)


## Toggles sub-scenes in Master Scene. Game will not load a new scene
func toggle_scene(scene_path: String, follow_history = true) -> void:
	if current_scene == scene_path:
		change_scene(prev_scene, follow_history)
	else:
		change_scene(scene_path, follow_history)


func set_master_scene(scene: PackedScene):
	_master_scene = scene


func _request_scene_change(scene_path: String, follow_history):
	# store prev scene
	var tree = get_tree()
	if follow_history:
		prev_scene = _get_current(tree)

	var err = tree.change_scene_to_file("res://"+ scene_path + ".tscn")

	if err != OK:
		print("[GameManager] Error: ", err, " ", scene_path)


func _get_current(tree: SceneTree) -> String:
	return tree.current_scene.scene_file_path.trim_prefix("res://").trim_suffix(".tscn")
