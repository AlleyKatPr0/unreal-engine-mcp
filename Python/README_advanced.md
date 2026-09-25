# Unreal MCP Advanced Server

A streamlined version of the Unreal MCP server that focuses only on advanced composition and building tools, reducing the total tool count from 44 to **21 tools**.

## What's Included

This server contains only the essential tools needed for advanced level building and composition:

### Essential Actor Management (8 tools)
- `get_actors_in_level()` - List all actors
- `find_actors_by_name(pattern)` - Find actors by pattern
- `delete_actor(name)` - Remove actors
- `set_actor_transform(name, location, rotation, scale)` - Modify transforms
- `batch_actor_operations(operations, continue_on_error)` - Spawn/update/delete in one command with per-item results
- `inspect_scene(summary_only, max_items, name_filter)` - Scene-aware summaries or detailed actor snapshots
- `inspect_actor_components(actor_name, summary_only)` - Inspect an actor with concise or full detail

### Essential Blueprint Tools (6 tools)
*Minimal set needed for physics actors*
- `create_blueprint(name, parent_class)` - Create Blueprint classes
- `add_component_to_blueprint()` - Add components to Blueprints
- `set_static_mesh_properties()` - Set mesh properties
- `set_physics_properties()` - Configure physics
- `compile_blueprint(name)` - Compile Blueprint changes
- `spawn_blueprint_actor()` - Spawn from Blueprint

### Advanced Composition Tools (10 tools)
*The main focus - advanced building and composition tools from the merge request*
- `create_pyramid(base_size, block_size, location, ...)` - Build pyramids
- `create_wall(length, height, block_size, location, orientation, ...)` - Generate walls
- `create_tower(levels, block_size, location, ...)` - Stack towers
- `create_staircase(steps, step_size, location, ...)` - Build staircases
- `construct_house(width, depth, height, location, ...)` - **Enhanced** game-ready houses
- `create_arch(radius, segments, location, ...)` - Arch structures
- `spawn_physics_blueprint_actor (name, mesh_path, location, mass, ...)` - Physics objects
- `create_maze(rows, cols, cell_size, wall_height, location, dry_run)` - Grid mazes with estimate mode
- `create_town(..., dry_run)` - Town generator with estimate mode
- `create_suspension_bridge(..., dry_run)` - Bridge generator with estimate mode
- `create_aqueduct(..., dry_run)` - Aqueduct generator with estimate mode

## AI-Assistant Focused Additions

- **Batch operations for fewer round trips:** `batch_actor_operations` accepts mixed spawn/transform/delete items and returns structured per-item status.
- **Preview before mutate:** high-volume generators expose `dry_run=True` estimation so models can plan actor cost before scene changes.
- **Structured output envelope:** new/updated paths use compact fields such as `success`, `status`, `message`, `metrics`, `results`, and `error`.
- **Scene awareness helpers:** use `inspect_scene` and `inspect_actor_components` to reason about existing scene state before generating more actors.

## Manual Validation Path

1. Call `create_town(town_size="medium", dry_run=True)` and confirm estimate-only output (`dry_run: true`, `metrics`, no spawned actors).
2. Call `create_maze(rows=8, cols=8, dry_run=True)` and confirm estimate details.
3. Run one `batch_actor_operations` request with mixed valid and invalid operations and verify partial result reporting per item.
4. Run `inspect_scene(summary_only=True)` then `inspect_scene(summary_only=False, max_items=5)` and confirm concise vs detailed output.

## Enhanced House Construction

The `construct_house` function has been significantly improved:

### Key Improvements:
- **Faster Spawning**: Uses large wall segments instead of individual blocks (20-30 actors vs 300+)
- **Realistic Proportions**: Default 12m x 10m x 6m house with proper room sizes
- **Smooth Walls**: Thin 20cm walls using scaled actors for clean appearance
- **Architectural Features**: 
  - Proper foundation and floor
  - Door opening (1.2m x 2.4m)
  - Window cutouts with proper placement
  - Pitched roof with realistic angle and overhang
  - Style-specific details (chimney, porch, garage)

### House Styles:
- **Modern**: Clean lines, garage door, flat details
- **Cottage**: Smaller size (80%), chimney, cozy proportions  
- **Mansion**: Larger size (150%), front porch with columns, chimney

### Example Usage:
```python
# Create a modern house
construct_house(house_style="modern")

# Create a cottage at specific location
construct_house(location=[1000, 0, 0], house_style="cottage")

# Create a large mansion
construct_house(width=1500, depth=1200, house_style="mansion")
```

## What's Removed

The following tool categories were removed to reduce complexity:
- UMG/Widget tools (5+ tools)
- Advanced Blueprint node management (8+ tools)
- Detailed physics material properties (3+ tools)
- Project configuration tools (2+ tools)
- Editor viewport/screenshot tools (3+ tools)
- Advanced component property setters (2+ tools)

## Usage

Run the streamlined server instead of the full one:

```bash
python unreal_mcp_server_advanced.py
```

## Benefits

- **Simpler**: Only 21 tools vs 44 tools
- **Focused**: Concentrates on advanced building/composition
- **Faster**: Reduced startup time and smaller tool list
- **Maintainable**: Easier to understand and modify
- **Self-contained**: No external tool dependencies

This server is perfect for users who primarily want to use the advanced composition tools for building complex structures, physics objects, and level layouts without the overhead of the full tool suite. 