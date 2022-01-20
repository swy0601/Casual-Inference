import net.sourceforge.squirrel_sql.fw.util.ICommand;
import net.sourceforge.squirrel_sql.fw.util.Resources;
import net.sourceforge.squirrel_sql.fw.util.StringManager;
import net.sourceforge.squirrel_sql.fw.util.StringManagerFactory;
import net.sourceforge.squirrel_sql.plugins.refactoring.commands.AddAutoIncrementCommand;

public class AddAutoIncrementAction extends AbstractRefactoringAction
{
	private static final long serialVersionUID = -5316665324698095673L;

	/**
	 * Internationalized strings for this class.
	 */
	private static final StringManager s_stringMgr =
		StringManagerFactory.getStringManager(AddAutoIncrementAction.class);

	private static interface i18n
	{
		String ACTION_PART = s_stringMgr.getString("AddAutoIncrementAction.actionPart");

		String OBJECT_PART = s_stringMgr.getString("Shared.tableObject");

		String SINGLE_OBJECT_MESSAGE =
			s_stringMgr.getString("Shared.singleObjectMessage", OBJECT_PART, ACTION_PART);
	}

	public AddAutoIncrementAction(final IApplication app, final Resources rsrc)
	{
		super(app, rsrc);
	}
