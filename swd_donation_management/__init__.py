from . import models


def pre_init_hook(cr):
    """Prepare legacy text values before converting swd_patient.name to many2one."""
    cr.execute(
        """
        SELECT data_type
          FROM information_schema.columns
         WHERE table_name = 'swd_patient'
           AND column_name = 'name'
        """
    )
    row = cr.fetchone()
    if not row:
        return

    data_type = row[0]
    if data_type in ("character varying", "text", "character"):
        cr.execute("UPDATE swd_patient SET name = NULL WHERE name IS NOT NULL")
