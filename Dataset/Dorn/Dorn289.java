		selenium.clickAt("//input[@value='Search']",
			RuntimeVariables.replace("Search"));
		selenium.waitForPageToLoad("30000");
		loadRequiredJavaScriptModules();
		assertEquals(RuntimeVariables.replace("Open"),
			selenium.getText("//td[2]/a"));
		selenium.clickAt("//td[2]/a", RuntimeVariables.replace("Open"));
		selenium.waitForPageToLoad("30000");
		loadRequiredJavaScriptModules();
		assertEquals(RuntimeVariables.replace("Test1 Folder1"),
			selenium.getText("//b"));
		selenium.clickAt("//b", RuntimeVariables.replace("Test1 Folder1"));
		selenium.waitForPageToLoad("30000");
		loadRequiredJavaScriptModules();
		selenium.clickAt("//input[@value='Add Document']",
			RuntimeVariables.replace("Add Document"));
		selenium.waitForPageToLoad("30000");
		loadRequiredJavaScriptModules();

		for (int second = 0;; second++) {
			if (second >= 90) {
				fail("timeout");
			}

			try {
				if (selenium.isVisible(
							"//a[@class='use-fallback using-new-uploader']")) {
					break;
				}
			}
			catch (Exception e) {
			}

			Thread.sleep(1000);
		}

		assertEquals(RuntimeVariables.replace("Use the classic uploader."),
			selenium.getText("//a[@class='use-fallback using-new-uploader']"));
		selenium.click("//a[@class='use-fallback using-new-uploader']");
		selenium.type("//input[@id='_20_file']",
			RuntimeVariables.replace(
				"L:\\portal\\build\\portal-web\\test\\com\\liferay\\portalweb\\portal\\dbupgrade\\sampledata523\\documentlibrary\\document\\dependencies\\test_document.txt"));
		selenium.type("//input[@id='_20_title']",
			RuntimeVariables.replace("Test1 Document1"));
		selenium.type("//textarea[@id='_20_description']",
			RuntimeVariables.replace("This is Test1 Document1"));
		selenium.clickAt("//input[@value='Save']",
			RuntimeVariables.replace("Save"));
		selenium.waitForPageToLoad("30000");
		loadRequiredJavaScriptModules();
