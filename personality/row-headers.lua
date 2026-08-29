-- Promote the first column of every table body to a row-header column.
-- Pandoc then emits <th scope="row"> instead of <td>, so a screen reader
-- announces "Self-Protection, N, .17*" rather than a bare number.
-- Opt a table out with the class .no-row-headers.
function Table(tbl)
  if tbl.classes and tbl.classes:includes("no-row-headers") then
    return nil
  end
  for _, body in ipairs(tbl.bodies) do
    body.row_head_columns = 1
  end
  return tbl
end
