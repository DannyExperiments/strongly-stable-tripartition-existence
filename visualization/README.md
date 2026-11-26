# Repair and stability

The Boolean cube shows which of A, A′ and C occur in the middle priority block at a fixed outer and universal assignment. Good has {A′}. The two Bad modes share {A} in this block and differ by two dummy markers in the last block. Repair has {A, C}. If Repair exists, the arrow marks its strict improvement over both Bad modes. Good still survives.

The example uses the matrix (x ∧ z) ∨ ¬y with one bit in each original block. Fix the outer padding bit s to zero, so changing the universal padding bit t has no effect. For x = 0, y = 1 has no repair, so the candidate ranking fails. For x = 1, both y values have a repair and both surviving modes induce the candidate ranking.

Extract the ZIP and open index.html. Choose x and y, then drag the cube or use the rotation slider. The text gives a concrete witness when one exists and shows the surviving modes for the selected challenge.

Run `python3 visualization/render.py` with Pillow and Arial fonts to rebuild the GIF and ZIP. Set `Q621_FONT_DIR` to the folder containing Arial.ttf and Arial Bold.ttf if those files are elsewhere.
